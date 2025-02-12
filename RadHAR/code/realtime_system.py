import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import datetime
import torch
import torch.nn as nn
import plotly.express as px
from collections import deque
import threading
import queue
import time
import cv2
from scipy import signal

# 3D点云可视化类
class PointCloudVisualizer:
    def __init__(self, max_points=1000):
        self.max_points = max_points
        self.points = deque(maxlen=max_points)
        self.colors = deque(maxlen=max_points)
        
    def update(self, new_points, new_intensities):
        """更新点云数据"""
        self.points.extend(new_points)
        normalized_intensities = (new_intensities - np.min(new_intensities)) / (np.max(new_intensities) - np.min(new_intensities))
        self.colors.extend(normalized_intensities)
        
    def get_figure(self):
        """生成3D点云图"""
        points = np.array(list(self.points))
        colors = np.array(list(self.colors))
        
        fig = go.Figure(data=[go.Scatter3d(
            x=points[:, 0],
            y=points[:, 1],
            z=points[:, 2],
            mode='markers',
            marker=dict(
                size=3,
                color=colors,
                colorscale='Viridis',
                opacity=0.8
            )
        )])
        
        fig.update_layout(
            scene=dict(
                xaxis_title="X轴 (米)",
                yaxis_title="Y轴 (米)",
                zaxis_title="Z轴 (米)",
                camera=dict(
                    up=dict(x=0, y=0, z=1),
                    center=dict(x=0, y=0, z=0),
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            showlegend=False,
            template="plotly_dark"
        )
        
        return fig

# 动作识别模型
class ActionRecognitionModel(nn.Module):
    def __init__(self, input_dim=12, hidden_dim=64, num_classes=5):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers=2, batch_first=True)
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(32, num_classes)
        )
        
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        return self.fc(lstm_out[:, -1, :])

# 实时数据处理器
class RealtimeProcessor:
    def __init__(self, model_path=None):
        self.point_cloud = PointCloudVisualizer()
        self.doppler_buffer = deque(maxlen=100)
        self.action_buffer = deque(maxlen=5)
        self.model = ActionRecognitionModel()
        if model_path:
            self.model.load_state_dict(torch.load(model_path))
        self.model.eval()
        
    def process_frame(self, frame_data):
        """处理单帧数据"""
        # 更新点云
        points = frame_data[:, :3]
        intensities = frame_data[:, -1]
        self.point_cloud.update(points, intensities)
        
        # 更新多普勒频谱
        velocity = frame_data[:, 7]  # 假设第8列是速度数据
        self.doppler_buffer.append(velocity)
        
        # 动作识别
        if len(self.doppler_buffer) == 100:
            features = np.array(list(self.doppler_buffer))
            with torch.no_grad():
                prediction = self.model(torch.FloatTensor(features).unsqueeze(0))
                action = torch.argmax(prediction).item()
                self.action_buffer.append(action)
        
        return self.get_visualization_data()
        
    def get_visualization_data(self):
        """获取可视化数据"""
        # 点云图
        point_cloud_fig = self.point_cloud.get_figure()
        
        # 多普勒频谱图
        if len(self.doppler_buffer) > 0:
            f, t, Sxx = signal.spectrogram(np.array(list(self.doppler_buffer)), fs=100)
            doppler_fig = go.Figure(data=[go.Heatmap(
                z=10 * np.log10(Sxx + 1e-10),
                x=t,
                y=f,
                colorscale='Jet'
            )])
            doppler_fig.update_layout(
                title="实时多普勒频谱图",
                xaxis_title="时间 (秒)",
                yaxis_title="频率 (Hz)",
                template="plotly_dark"
            )
        else:
            doppler_fig = go.Figure()
        
        # 动作识别结果
        action_names = ['拳击', '开合跳', '跳跃', '深蹲', '行走']
        if len(self.action_buffer) > 0:
            action = max(set(self.action_buffer), key=list(self.action_buffer).count)
            action_name = action_names[action]
        else:
            action_name = "等待识别..."
        
        return point_cloud_fig, doppler_fig, action_name

# 创建Dash应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("RadHAR 实时人类活动识别系统", className="text-center mb-4"), width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H3("3D点云实时可视化", className="text-center"),
            dcc.Graph(id='point-cloud-graph')
        ], width=6),
        
        dbc.Col([
            html.H3("多普勒频谱实时分析", className="text-center"),
            dcc.Graph(id='doppler-graph')
        ], width=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H3("当前识别结果", className="text-center"),
            html.Div(id='action-result', className="text-center h1")
        ], width=12)
    ]),
    
    dcc.Interval(id='interval-component', interval=100),  # 100ms更新一次
], fluid=True, style={'backgroundColor': '#1a1a1a', 'color': 'white'})

# 数据模拟器
class DataSimulator:
    def __init__(self):
        self.time = 0
        
    def get_next_frame(self):
        """模拟生成下一帧数据"""
        num_points = np.random.randint(50, 200)
        
        # 生成3D点云数据
        x = np.random.normal(0, 0.5, num_points)
        y = np.random.normal(0, 0.5, num_points)
        z = np.abs(np.random.normal(1, 0.2, num_points))
        
        # 生成速度和强度数据
        velocity = np.sin(self.time + np.random.normal(0, 0.1, num_points))
        intensity = np.abs(np.random.normal(30, 5, num_points))
        
        self.time += 0.1
        
        return np.column_stack([x, y, z, velocity, intensity])

# 创建处理器和模拟器实例
processor = RealtimeProcessor()
simulator = DataSimulator()

@app.callback(
    [Output('point-cloud-graph', 'figure'),
     Output('doppler-graph', 'figure'),
     Output('action-result', 'children')],
    Input('interval-component', 'n_intervals')
)
def update_graphs(n):
    """更新所有图表"""
    # 获取新的数据帧
    frame_data = simulator.get_next_frame()
    
    # 处理数据并获取可视化结果
    point_cloud_fig, doppler_fig, action = processor.process_frame(frame_data)
    
    # 设置动作识别结果的样式
    action_html = html.Div([
        html.P("当前识别的动作：", style={'fontSize': '20px'}),
        html.P(action, style={
            'fontSize': '32px',
            'fontWeight': 'bold',
            'color': '#00ff00'
        })
    ])
    
    return point_cloud_fig, doppler_fig, action_html

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
