"""Comprehensive verification of model results and performance metrics."""

import os
import time
import torch
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from data.package.models.hierarchical_attention import HierarchicalAttention
from data.package.models.domain_adaptation import MultiScaleDomainAdapter
from data.package.configs.model_config import Config
from data_loader import create_dataloaders

def load_latest_checkpoint(model, domain_adapter, checkpoint_dir):
    """Load the latest checkpoint."""
    checkpoints = sorted([f for f in os.listdir(checkpoint_dir) if f.endswith('.pth')])
    if not checkpoints:
        raise ValueError("No checkpoints found")
    
    latest_checkpoint = os.path.join(checkpoint_dir, checkpoints[-1])
    print(f"Loading checkpoint: {latest_checkpoint}")
    checkpoint = torch.load(latest_checkpoint)
    
    model.load_state_dict(checkpoint['model_state_dict'])
    domain_adapter.load_state_dict(checkpoint['domain_adapter_state_dict'])
    return checkpoint['metrics']

def analyze_training_convergence(metrics):
    """Analyze training convergence and plot metrics."""
    plt.figure(figsize=(15, 10))
    
    # Plot training and validation loss
    plt.subplot(2, 2, 1)
    plt.plot(metrics['train_loss'], label='Train Loss')
    plt.plot(metrics['val_loss'], label='Val Loss')
    plt.title('Training Convergence')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    # Plot accuracy
    plt.subplot(2, 2, 2)
    plt.plot(metrics['accuracy'], label='Accuracy')
    plt.axhline(y=91.7, color='r', linestyle='--', label='Target (91.7%)')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy (%)')
    plt.legend()
    
    # Plot domain adaptation score
    plt.subplot(2, 2, 3)
    plt.plot(metrics['domain_score'], label='Domain Score')
    plt.axhline(y=0.746, color='r', linestyle='--', label='Target (0.746)')
    plt.title('Domain Adaptation Score')
    plt.xlabel('Epoch')
    plt.ylabel('Score')
    plt.legend()
    
    plt.tight_layout()
    os.makedirs('visualizations', exist_ok=True)
    plt.savefig('visualizations/training_metrics.png')
    plt.close()

def measure_inference_performance(model, domain_adapter, val_loader, num_samples=100):
    """Measure inference latency and memory usage."""
    model.eval()
    domain_adapter.eval()
    latencies = []
    memory_usages = []
    
    with torch.no_grad():
        for i, (data, _) in enumerate(tqdm(val_loader, desc="Measuring Performance")):
            if i >= num_samples:
                break
            
            # Measure latency
            start_time = time.time()
            features = model(data)
            output = domain_adapter(features)
            latency = (time.time() - start_time) * 1000  # Convert to ms
            latencies.append(latency)
            
            # Measure memory
            if torch.cuda.is_available():
                memory_mb = torch.cuda.memory_allocated() / (1024 * 1024)
            else:
                import psutil
                memory_mb = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
            memory_usages.append(memory_mb)
    
    avg_latency = np.mean(latencies)
    avg_memory = np.mean(memory_usages)
    max_memory = np.max(memory_usages)
    
    return {
        'avg_latency': avg_latency,
        'avg_memory': avg_memory,
        'max_memory': max_memory
    }

def verify_results():
    """Verify all model results and performance metrics."""
    print("Starting comprehensive result verification...")
    
    # Load configuration and setup
    config = Config()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Initialize models
    model = HierarchicalAttention(config).to(device)
    domain_adapter = MultiScaleDomainAdapter(config).to(device)
    
    # Load checkpoint and metrics
    checkpoint_dir = os.path.join(os.path.dirname(__file__), '..', 'checkpoints')
    metrics = load_latest_checkpoint(model, domain_adapter, checkpoint_dir)
    
    # Analyze training convergence
    print("\nAnalyzing training convergence...")
    analyze_training_convergence(metrics)
    
    # Create data loader
    _, val_loader = create_dataloaders(config)
    
    # Measure performance
    print("\nMeasuring inference performance...")
    perf_metrics = measure_inference_performance(model, domain_adapter, val_loader)
    
    # Print final results
    print("\nFinal Results:")
    print("-" * 50)
    print(f"Model Accuracy: {metrics['accuracy'][-1]:.2f}% (target: >91.7%)")
    print(f"Domain Score: {metrics['domain_score'][-1]:.3f} (target: >0.746)")
    print(f"Inference Latency: {perf_metrics['avg_latency']:.2f}ms (target: <50ms)")
    print(f"Memory Usage: {perf_metrics['avg_memory']:.2f}MB (target: <2048MB)")
    print("-" * 50)
    
    # Verify targets
    targets_met = {
        'accuracy': metrics['accuracy'][-1] > 91.7,
        'domain_score': metrics['domain_score'][-1] > 0.746,
        'latency': perf_metrics['avg_latency'] < 50,
        'memory': perf_metrics['max_memory'] < 2048
    }
    
    print("\nTarget Status:")
    for metric, met in targets_met.items():
        status = "✓" if met else "✗"
        print(f"{metric}: {status}")

if __name__ == '__main__':
    verify_results()
