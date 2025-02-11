"""Training monitoring and visualization system for RadHAR."""

import os
import time
import psutil
import numpy as np
import torch
from datetime import datetime
import matplotlib.pyplot as plt
from PyQt5.QtCore import QObject, pyqtSignal

class PerformanceMetrics:
    """Track and store performance metrics."""
    def __init__(self):
        self.metrics = {
            'train_loss': [],
            'val_loss': [],
            'accuracy': [],
            'domain_score': [],
            'inference_latency': [],
            'memory_usage': [],
            'feature_extraction_time': [],
            'attention_computation_time': [],
            'domain_adaptation_time': []
        }
        
        self.targets = {
            'inference_latency': 50.0,  # ms
            'memory_usage': 2048.0,     # MB
            'accuracy': 91.7,           # %
            'domain_score': 0.746
        }
    
    def update(self, metric_name, value):
        """Update a specific metric."""
        if metric_name in self.metrics:
            self.metrics[metric_name].append(value)
    
    def get_latest(self, metric_name):
        """Get the latest value for a metric."""
        if metric_name in self.metrics and self.metrics[metric_name]:
            return self.metrics[metric_name][-1]
        return None
    
    def check_targets(self):
        """Check if performance targets are met."""
        results = {}
        for metric, target in self.targets.items():
            current = self.get_latest(metric)
            if current is not None:
                results[metric] = {
                    'current': current,
                    'target': target,
                    'met': (current <= target if metric in ['inference_latency', 'memory_usage']
                           else current >= target)
                }
        return results

class TrainingMonitor(QObject):
    """Monitor and visualize training progress."""
    # Define signals for GUI updates
    update_signal = pyqtSignal(dict)
    
    def __init__(self, config, log_dir='logs'):
        super().__init__()
        self.config = config
        self.log_dir = log_dir
        self.metrics = PerformanceMetrics()
        self.start_time = time.time()
        
        # Create log directory
        os.makedirs(log_dir, exist_ok=True)
        
        # Initialize logging
        self.log_file = os.path.join(
            log_dir, 
            f'training_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        )
    
    def log_metrics(self, epoch, batch_idx, metrics_dict):
        """Log training metrics."""
        # Update metrics
        for metric_name, value in metrics_dict.items():
            self.metrics.update(metric_name, value)
        
        # Log to file
        with open(self.log_file, 'a') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_str = f"[{timestamp}] Epoch {epoch} Batch {batch_idx}: "
            log_str += ", ".join([f"{k}: {v:.4f}" for k, v in metrics_dict.items()])
            f.write(log_str + '\n')
        
        # Check performance targets
        target_status = self.metrics.check_targets()
        
        # Prepare data for GUI update
        update_data = {
            'metrics': metrics_dict,
            'targets': target_status,
            'epoch': epoch,
            'batch': batch_idx,
            'elapsed_time': time.time() - self.start_time
        }
        
        # Emit signal for GUI update
        self.update_signal.emit(update_data)
    
    def measure_inference_time(self, func):
        """Measure inference time of a function."""
        start_time = time.time()
        result = func()
        inference_time = (time.time() - start_time) * 1000  # Convert to ms
        self.metrics.update('inference_latency', inference_time)
        return result
    
    def measure_memory_usage(self):
        """Measure current memory usage."""
        process = psutil.Process(os.getpid())
        memory_mb = process.memory_info().rss / 1024 / 1024  # Convert to MB
        self.metrics.update('memory_usage', memory_mb)
        return memory_mb
    
    def plot_metrics(self, save_dir='visualizations'):
        """Generate and save visualization plots."""
        os.makedirs(save_dir, exist_ok=True)
        
        # Plot training metrics
        plt.figure(figsize=(12, 8))
        plt.subplot(2, 2, 1)
        plt.plot(self.metrics.metrics['train_loss'], label='Train Loss')
        plt.plot(self.metrics.metrics['val_loss'], label='Val Loss')
        plt.title('Training Loss')
        plt.legend()
        
        plt.subplot(2, 2, 2)
        plt.plot(self.metrics.metrics['accuracy'], label='Accuracy')
        plt.axhline(y=self.metrics.targets['accuracy'], color='r', linestyle='--', 
                   label='Target')
        plt.title('Accuracy')
        plt.legend()
        
        plt.subplot(2, 2, 3)
        plt.plot(self.metrics.metrics['inference_latency'], label='Latency')
        plt.axhline(y=self.metrics.targets['inference_latency'], color='r', 
                   linestyle='--', label='Target')
        plt.title('Inference Latency (ms)')
        plt.legend()
        
        plt.subplot(2, 2, 4)
        plt.plot(self.metrics.metrics['domain_score'], label='Domain Score')
        plt.axhline(y=self.metrics.targets['domain_score'], color='r', 
                   linestyle='--', label='Target')
        plt.title('Domain Adaptation Score')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, 'training_metrics.png'))
        plt.close()
    
    def save_metrics(self, filename='metrics.npz'):
        """Save metrics to file."""
        save_path = os.path.join(self.log_dir, filename)
        np.savez(save_path, **self.metrics.metrics)
    
    def load_metrics(self, filename='metrics.npz'):
        """Load metrics from file."""
        load_path = os.path.join(self.log_dir, filename)
        if os.path.exists(load_path):
            data = np.load(load_path)
            for key in data.files:
                self.metrics.metrics[key] = data[key].tolist()

def create_training_monitor(config):
    """Create and initialize training monitor."""
    return TrainingMonitor(config)

if __name__ == '__main__':
    # Test monitoring system
    from data.package.configs.model_config import Config
    config = Config()
    monitor = create_training_monitor(config)
    
    # Simulate some metrics
    for i in range(10):
        metrics = {
            'train_loss': np.random.random(),
            'val_loss': np.random.random(),
            'accuracy': 90 + np.random.random() * 5,
            'domain_score': 0.7 + np.random.random() * 0.1,
            'inference_latency': 45 + np.random.random() * 10
        }
        monitor.log_metrics(0, i, metrics)
    
    # Generate test plots
    monitor.plot_metrics()
