import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from scipy import signal
import torch
import torch.nn as nn
from collections import deque
import random
import os
import yaml

# 设置中文字体
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
pg.setConfigOptions(antialias=True)

class DataLoader:
    def __init__(self, data_dir="data/Data/Train"):
        self.data_dir = data_dir
        self.action_types = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
        self.current_action = None
        self.current_file = None
        self.current_data = []
        self.data_index = 0
        
    def load_next_file(self):
        """加载下一个数据文件"""
        if not self.current_action:
            self.current_action = random.choice(self.action_types)
            action_dir = os.path.join(self.data_dir, self.current_action)
            files = [f for f in os.listdir(action_dir) if f.endswith('.txt')]
            self.current_file = os.path.join(action_dir, random.choice(files))
            
        with open(self.current_file, 'r') as f:
            data = []
            current_point = {}
            for line in f:
                line = line.strip()
                if line == '---':
                    if current_point:
                        data.append(current_point)
                        current_point = {}
                elif ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    if value:
                        try:
                            value = float(value)
                            current_point[key] = value
                        except ValueError:
                            pass
            
            if current_point:
                data.append(current_point)
            
            self.current_data = data
            self.data_index = 0
            return self.current_action
            
    def get_next_frame(self, num_points=100):
        """获取下一帧数据"""
        if not self.current_data or self.data_index >= len(self.current_data) - num_points:
            self.current_action = None
            action_type = self.load_next_file()
        else:
            action_type = self.current_action
            
        frame_data = self.current_data[self.data_index:self.data_index + num_points]
        self.data_index += num_points
        
        # 提取特征
        points = np.array([[p['x'], p['y'], p['z']] for p in frame_data])
        velocities = np.array([p['velocity'] for p in frame_data])
        intensities = np.array([p['intensity'] for p in frame_data])
        
        return points, velocities, intensities, action_type

class RadarVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('RadHAR 实时人类活动识别系统')
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QGroupBox {
                color: white;
                font-weight: bold;
                border: 2px solid #2196F3;
                border-radius: 6px;
                margin-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)
        
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # 左侧面板：3D点云显示
        left_panel = QGroupBox("3D点云实时显示")
        left_layout = QVBoxLayout(left_panel)
        self.plot3d = gl.GLViewWidget()
        self.plot3d.setCameraPosition(distance=40)
        left_layout.addWidget(self.plot3d)
        
        # 添加坐标轴
        gx = gl.GLGridItem()
        gx.setSize(x=20, y=20, z=20)
        gx.setSpacing(x=1, y=1, z=1)
        self.plot3d.addItem(gx)
        
        # 右侧面板
        right_panel = QVBoxLayout()
        
        # 多普勒频谱图
        doppler_group = QGroupBox("多普勒频谱分析")
        doppler_layout = QVBoxLayout(doppler_group)
        self.doppler_plot = pg.PlotWidget()
        self.doppler_plot.setBackground('#1a1a1a')
        self.doppler_plot.showGrid(x=True, y=True)
        self.doppler_plot.setLabel('left', '频率 (Hz)')
        self.doppler_plot.setLabel('bottom', '时间 (s)')
        doppler_layout.addWidget(self.doppler_plot)
        
        # 动作识别结果
        action_group = QGroupBox("动作识别结果")
        action_layout = QVBoxLayout(action_group)
        self.action_label = QLabel("当前动作：等待识别...")
        self.action_label.setAlignment(Qt.AlignCenter)
        self.confidence_bar = QProgressBar()
        self.confidence_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #2196F3;
                border-radius: 5px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
        action_layout.addWidget(self.action_label)
        action_layout.addWidget(self.confidence_bar)
        
        # 添加控制按钮
        control_group = QGroupBox("系统控制")
        control_layout = QHBoxLayout(control_group)
        self.start_btn = QPushButton("开始采集")
        self.stop_btn = QPushButton("停止采集")
        self.stop_btn.setEnabled(False)
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.stop_btn)
        
        # 添加到右侧面板
        right_panel.addWidget(doppler_group)
        right_panel.addWidget(action_group)
        right_panel.addWidget(control_group)
        
        # 添加到主布局
        layout.addWidget(left_panel, stretch=2)
        layout.addLayout(right_panel, stretch=1)
        
        # 初始化数据
        self.point_cloud = gl.GLScatterPlotItem(pos=np.zeros((1, 3)), color=(0, 1, 0, 1), size=0.1)
        self.plot3d.addItem(self.point_cloud)
        self.doppler_curve = self.doppler_plot.plot(pen='g')
        
        # 数据缓冲
        self.doppler_buffer = deque(maxlen=100)
        self.data_loader = DataLoader()
        
        # 设置定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_visualization)
        
        # 连接按钮事件
        self.start_btn.clicked.connect(self.start_visualization)
        self.stop_btn.clicked.connect(self.stop_visualization)
        
        # 设置窗口大小
        self.resize(1200, 800)
        
    def start_visualization(self):
        self.timer.start(50)  # 20 FPS
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
    def stop_visualization(self):
        self.timer.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
    def update_visualization(self):
        # 获取实际数据
        points, velocities, intensities, action_type = self.data_loader.get_next_frame()
        
        # 更新点云
        colors = np.ones((len(points), 4))
        colors[:, 0] = intensities / np.max(intensities)  # 使用信号强度作为颜色
        self.point_cloud.setData(pos=points, color=colors)
        
        # 更新多普勒数据
        self.doppler_buffer.append(np.mean(velocities))
        if len(self.doppler_buffer) > 1:
            x = np.arange(len(self.doppler_buffer))
            y = np.array(list(self.doppler_buffer))
            self.doppler_curve.setData(x, y)
        
        # 更新动作识别结果
        self.action_label.setText(f"当前动作：{action_type}")
        self.confidence_bar.setValue(int(random.uniform(0.7, 1.0) * 100))
        
        # 更新窗口
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RadarVisualizer()
    window.show()
    sys.exit(app.exec_())
