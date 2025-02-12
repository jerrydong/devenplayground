"""Generate comprehensive performance analysis and visualizations."""

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import torch
from data.package.models.hierarchical_attention import HierarchicalAttention
from data.package.models.domain_adaptation import MultiScaleDomainAdapter
from data.package.configs.model_config import Config
from data_loader import create_dataloaders

def plot_training_metrics(metrics, save_dir='visualizations'):
    """Plot training metrics over time."""
    os.makedirs(save_dir, exist_ok=True)
    
    plt.figure(figsize=(15, 10))
    
    # Plot training loss
    plt.subplot(2, 2, 1)
    plt.plot(metrics['train_loss'], label='Training Loss')
    plt.plot(metrics['val_loss'], label='Validation Loss')
    plt.title('Loss Curves')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    
    # Plot accuracy
    plt.subplot(2, 2, 2)
    plt.plot(metrics['accuracy'], label='Model Accuracy')
    plt.axhline(y=91.7, color='r', linestyle='--', label='Target (91.7%)')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy (%)')
    plt.legend()
    plt.grid(True)
    
    # Plot domain score
    plt.subplot(2, 2, 3)
    plt.plot(metrics['domain_score'], label='Domain Score')
    plt.axhline(y=0.746, color='r', linestyle='--', label='Target (0.746)')
    plt.title('Domain Adaptation Score')
    plt.xlabel('Epoch')
    plt.ylabel('Score')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'training_metrics.png'))
    plt.close()

def generate_confusion_matrix(model, domain_adapter, val_loader, save_dir='visualizations'):
    """Generate and plot confusion matrix."""
    model.eval()
    domain_adapter.eval()
    
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for data, labels in val_loader:
            features = model(data)
            outputs = domain_adapter(features)
            _, preds = torch.max(outputs, 1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    # Create confusion matrix
    cm = confusion_matrix(all_labels, all_preds)
    
    # Plot confusion matrix
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.savefig(os.path.join(save_dir, 'confusion_matrix.png'))
    plt.close()
    
    return cm

def analyze_per_class_performance(cm, save_dir='visualizations'):
    """Analyze and plot per-class performance metrics."""
    # Calculate per-class metrics
    per_class_acc = np.diag(cm) / np.sum(cm, axis=1)
    
    # Plot per-class accuracy
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(per_class_acc)), per_class_acc * 100)
    plt.axhline(y=91.7, color='r', linestyle='--', label='Target (91.7%)')
    plt.title('Per-Class Accuracy')
    plt.xlabel('Class Index')
    plt.ylabel('Accuracy (%)')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(save_dir, 'per_class_accuracy.png'))
    plt.close()
    
    return per_class_acc

def main():
    """Generate comprehensive analysis and visualizations."""
    print("Generating performance analysis and visualizations...")
    
    # Setup
    config = Config()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Initialize models
    model = HierarchicalAttention(config).to(device)
    domain_adapter = MultiScaleDomainAdapter(config).to(device)
    
    # Load checkpoint
    checkpoint_dir = os.path.join(os.path.dirname(__file__), '..', 'checkpoints')
    checkpoints = sorted([f for f in os.listdir(checkpoint_dir) if f.endswith('.pth')])
    if checkpoints:
        checkpoint = torch.load(os.path.join(checkpoint_dir, checkpoints[-1]))
        model.load_state_dict(checkpoint['model_state_dict'])
        domain_adapter.load_state_dict(checkpoint['domain_adapter_state_dict'])
        metrics = checkpoint['metrics']
        
        # Create visualizations directory
        os.makedirs('visualizations', exist_ok=True)
        
        # Generate plots
        plot_training_metrics(metrics)
        
        # Load validation data
        _, val_loader = create_dataloaders(config)
        
        # Generate confusion matrix
        cm = generate_confusion_matrix(model, domain_adapter, val_loader)
        
        # Analyze per-class performance
        per_class_acc = analyze_per_class_performance(cm)
        
        # Print summary
        print("\nPerformance Summary:")
        print("-" * 50)
        print(f"Final Accuracy: {metrics['accuracy'][-1]:.2f}%")
        print(f"Final Domain Score: {metrics['domain_score'][-1]:.3f}")
        print(f"Average Per-Class Accuracy: {np.mean(per_class_acc)*100:.2f}%")
        print("-" * 50)
        print("\nVisualization files have been saved to the 'visualizations' directory.")

if __name__ == '__main__':
    main()
