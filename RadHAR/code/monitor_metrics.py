"""Real-time performance monitoring for RadHAR training."""

import os
import time
import psutil
import torch
import numpy as np
from tqdm import tqdm
from data.package.models.hierarchical_attention import HierarchicalAttention
from data.package.models.domain_adaptation import MultiScaleDomainAdapter
from data.package.configs.model_config import Config
from data_loader import create_dataloaders

def measure_inference_latency(model, domain_adapter, data_loader, num_samples=100, device='cpu'):
    """Measure inference latency."""
    model.eval()
    domain_adapter.eval()
    latencies = []
    
    with torch.no_grad():
        for i, (data, _) in enumerate(data_loader):
            if i >= num_samples:
                break
                
            data = data.to(device)
            
            # Measure inference time
            start_time = time.time()
            features = model(data)
            output = domain_adapter(features)
            end_time = time.time()
            
            latency = (end_time - start_time) * 1000  # Convert to ms
            latencies.append(latency)
    
    avg_latency = np.mean(latencies)
    print(f"Average inference latency: {avg_latency:.2f}ms (target: <50ms)")
    return avg_latency

def measure_memory_usage(model, domain_adapter, data_loader, num_samples=100, device='cpu'):
    """Measure memory usage."""
    model.eval()
    domain_adapter.eval()
    memory_usages = []
    
    with torch.no_grad():
        for i, (data, _) in enumerate(data_loader):
            if i >= num_samples:
                break
                
            data = data.to(device)
            
            # Clear cache
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            # Measure memory before inference
            process = psutil.Process(os.getpid())
            start_mem = process.memory_info().rss / (1024 * 1024)  # MB
            
            # Run inference
            features = model(data)
            output = domain_adapter(features)
            
            # Measure memory after inference
            end_mem = process.memory_info().rss / (1024 * 1024)  # MB
            memory_usage = end_mem - start_mem
            memory_usages.append(memory_usage)
    
    avg_memory = np.mean(memory_usages)
    print(f"Average memory usage: {avg_memory:.2f}MB (target: <2048MB)")
    return avg_memory

def monitor_performance():
    """Monitor model performance metrics."""
    # Load configuration
    config = Config()
    
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Initialize models
    model = HierarchicalAttention(config).to(device)
    domain_adapter = MultiScaleDomainAdapter(config).to(device)
    
    # Setup checkpoint directory
    checkpoint_dir = os.path.join(os.path.dirname(__file__), '..', 'checkpoints')
    os.makedirs(checkpoint_dir, exist_ok=True)
    print(f"Looking for checkpoints in: {checkpoint_dir}")
    
    # Check if training is in progress
    training_pid_file = os.path.join(checkpoint_dir, 'training.pid')
    if os.path.exists(training_pid_file):
        with open(training_pid_file, 'r') as f:
            pids = [int(pid.strip()) for pid in f.readlines() if pid.strip()]
            running_pids = [pid for pid in pids if psutil.pid_exists(pid)]
            if running_pids:
                print(f"Training process is running (PIDs: {running_pids})")
    
    # Load latest checkpoint
    try:
        checkpoints = sorted([f for f in os.listdir(checkpoint_dir) if f.endswith('.pth')])
        if checkpoints:
            latest_checkpoint = os.path.join(checkpoint_dir, checkpoints[-1])
            print(f"Loading checkpoint: {latest_checkpoint}")
            checkpoint = torch.load(latest_checkpoint)
            model.load_state_dict(checkpoint['model_state_dict'])
            domain_adapter.load_state_dict(checkpoint['domain_adapter_state_dict'])
            print("Model weights loaded successfully")
            
            # Get metrics from checkpoint
            metrics = checkpoint['metrics']
            latest_accuracy = metrics['accuracy'][-1] if metrics['accuracy'] else 0
            latest_domain_score = metrics['domain_score'][-1] if metrics['domain_score'] else 0
            print(f"Latest accuracy: {latest_accuracy:.2f}% (target: >91.7%)")
            print(f"Latest domain score: {latest_domain_score:.3f} (target: >0.746)")
        else:
            print("No checkpoints found. Using initialized model.")
            latest_accuracy = 0
            latest_domain_score = 0
    except Exception as e:
        print(f"Error loading checkpoint: {e}")
        print("Using initialized model.")
        latest_accuracy = 0
        latest_domain_score = 0
    
    print("\nCreating validation data loader...")
    _, val_loader = create_dataloaders(config)
    
    # Measure performance metrics
    latency = measure_inference_latency(model, domain_adapter, val_loader)
    memory = measure_memory_usage(model, domain_adapter, val_loader)
    
    # Print summary
    print("\nPerformance Summary:")
    print("-" * 50)
    print(f"Inference Latency: {latency:.2f}ms (target: <50ms)")
    print(f"Memory Usage: {memory:.2f}MB (target: <2048MB)")
    if checkpoints:
        print(f"Model Accuracy: {latest_accuracy:.2f}% (target: >91.7%)")
        print(f"Domain Score: {latest_domain_score:.3f} (target: >0.746)")
    print("-" * 50)

if __name__ == '__main__':
    monitor_performance()
