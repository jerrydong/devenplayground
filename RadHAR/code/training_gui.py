"""GUI system for RadHAR training visualization and monitoring."""

import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QHBoxLayout, QLabel, QProgressBar)
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg

class MetricsPlot(pg.PlotWidget):
    """Plot widget for training metrics."""
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setBackground('w')
        self.setTitle(title, color='k')
        self.showGrid(x=True, y=True)
        self.setLabel('left', 'Value', color='k')
        self.setLabel('bottom', 'Iteration', color='k')
        self.addLegend()
        
        # Store plot curves
        self.curves = {}
    
    def update_plot(self, data_dict):
        """Update plot with new data."""
        for name, values in data_dict.items():
            if name not in self.curves:
                self.curves[name] = self.plot(
                    values,
                    name=name,
                    pen=pg.mkPen(color=self.get_color(name), width=2)
                )
            else:
                self.curves[name].setData(values)
    
    def get_color(self, name):
        """Get color for plot line."""
        colors = {
            'train_loss': (255, 0, 0),
            'val_loss': (0, 0, 255),
            'accuracy': (0, 255, 0),
            'domain_score': (128, 0, 128)
        }
        return colors.get(name, (0, 0, 0))

class PerformanceWidget(QWidget):
    """Widget for displaying performance metrics."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI layout."""
        layout = QVBoxLayout()
        
        # Create performance indicators
        self.indicators = {
            'inference_latency': self.create_indicator('Inference Latency (ms)', 50),
            'memory_usage': self.create_indicator('Memory Usage (MB)', 2048),
            'accuracy': self.create_indicator('Accuracy (%)', 91.7),
            'domain_score': self.create_indicator('Domain Score', 0.746)
        }
        
        for indicator in self.indicators.values():
            layout.addWidget(indicator)
        
        self.setLayout(layout)
    
    def create_indicator(self, name, target):
        """Create a performance indicator widget."""
        widget = QWidget()
        layout = QHBoxLayout()
        
        # Label
        label = QLabel(f"{name}:")
        layout.addWidget(label)
        
        # Progress bar
        progress = QProgressBar()
        progress.setTextVisible(True)
        progress.setMaximum(int(target * 100))
        layout.addWidget(progress)
        
        # Target label
        target_label = QLabel(f"Target: {target}")
        layout.addWidget(target_label)
        
        widget.setLayout(layout)
        return {'widget': widget, 'progress': progress, 'target': target}
    
    def update_indicators(self, metrics):
        """Update performance indicators."""
        for name, value in metrics.items():
            if name in self.indicators:
                indicator = self.indicators[name]
                progress = indicator['progress']
                target = indicator['target']
                
                # Update progress bar
                progress.setValue(int(value * 100))
                progress.setFormat(f'{value:.2f} / {target:.2f}')
                
                # Set color based on target
                if name in ['inference_latency', 'memory_usage']:
                    met_target = value <= target
                else:
                    met_target = value >= target
                
                style = """
                    QProgressBar {
                        text-align: center;
                    }
                    QProgressBar::chunk {
                        background-color: %s;
                    }
                """ % ('green' if met_target else 'red')
                
                progress.setStyleSheet(style)

class TrainingGUI(QMainWindow):
    """Main GUI window for training visualization."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle('RadHAR Training Monitor')
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI layout."""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Add plots
        plots_layout = QHBoxLayout()
        
        # Loss plot
        self.loss_plot = MetricsPlot('Training Loss')
        plots_layout.addWidget(self.loss_plot)
        
        # Accuracy plot
        self.accuracy_plot = MetricsPlot('Model Performance')
        plots_layout.addWidget(self.accuracy_plot)
        
        layout.addLayout(plots_layout)
        
        # Add performance indicators
        self.performance_widget = PerformanceWidget()
        layout.addWidget(self.performance_widget)
        
        central_widget.setLayout(layout)
        
        # Set window size
        self.resize(1200, 800)
        
        # Setup update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_plots)
        self.update_timer.start(1000)  # Update every second
    
    def update_plots(self):
        """Update plots with new data."""
        # This will be connected to the training monitor
        pass
    
    def update_metrics(self, metrics_data):
        """Update all visualizations with new metrics."""
        # Update loss plot
        loss_data = {
            'train_loss': metrics_data.get('train_loss', []),
            'val_loss': metrics_data.get('val_loss', [])
        }
        self.loss_plot.update_plot(loss_data)
        
        # Update performance plot
        perf_data = {
            'accuracy': metrics_data.get('accuracy', []),
            'domain_score': metrics_data.get('domain_score', [])
        }
        self.accuracy_plot.update_plot(perf_data)
        
        # Update performance indicators
        latest_metrics = {
            'inference_latency': metrics_data.get('inference_latency', [])[-1],
            'memory_usage': metrics_data.get('memory_usage', [])[-1],
            'accuracy': metrics_data.get('accuracy', [])[-1],
            'domain_score': metrics_data.get('domain_score', [])[-1]
        }
        self.performance_widget.update_indicators(latest_metrics)

def create_training_gui():
    """Create and initialize training GUI."""
    app = QApplication(sys.argv)
    gui = TrainingGUI()
    gui.show()
    return app, gui

if __name__ == '__main__':
    # Test GUI
    app, gui = create_training_gui()
    
    # Simulate some data
    def update_test_data():
        metrics = {
            'train_loss': list(np.random.rand(100)),
            'val_loss': list(np.random.rand(100)),
            'accuracy': list(90 + np.random.rand(100) * 5),
            'domain_score': list(0.7 + np.random.rand(100) * 0.1),
            'inference_latency': 45.0,
            'memory_usage': 1800.0
        }
        gui.update_metrics(metrics)
    
    # Setup test timer
    timer = QTimer()
    timer.timeout.connect(update_test_data)
    timer.start(1000)
    
    sys.exit(app.exec_())
