"""Parse training output to verify results during training."""

import re
import os
import numpy as np
import matplotlib.pyplot as plt

def parse_training_output(output_file):
    """Parse training output file to extract metrics."""
    metrics = {
        'batch_losses': [],
        'batch_accuracies': [],
        'epochs': [],
        'current_epoch': 0
    }
    
    with open(output_file, 'r') as f:
        for line in f:
            # Parse batch metrics
            batch_match = re.search(r'Train Batch \[(\d+)/\d+\] Loss: ([\d.]+) Acc: ([\d.]+)%', line)
            if batch_match:
                batch_num = int(batch_match.group(1))
                loss = float(batch_match.group(2))
                acc = float(batch_match.group(3))
                metrics['batch_losses'].append(loss)
                metrics['batch_accuracies'].append(acc)
            
            # Parse epoch info
            epoch_match = re.search(r'Epoch (\d+)/\d+', line)
            if epoch_match:
                metrics['current_epoch'] = int(epoch_match.group(1))
                metrics['epochs'].append(metrics['current_epoch'])
    
    return metrics

def plot_training_progress(metrics, output_dir='visualizations'):
    """Plot training progress metrics."""
    os.makedirs(output_dir, exist_ok=True)
    
    plt.figure(figsize=(12, 8))
    
    # Plot loss
    plt.subplot(2, 1, 1)
    plt.plot(metrics['batch_losses'], label='Training Loss')
    plt.title('Training Loss Progress')
    plt.xlabel('Batch')
    plt.ylabel('Loss')
    plt.legend()
    
    # Plot accuracy
    plt.subplot(2, 1, 2)
    plt.plot(metrics['batch_accuracies'], label='Training Accuracy')
    plt.axhline(y=91.7, color='r', linestyle='--', label='Target (91.7%)')
    plt.title('Training Accuracy Progress')
    plt.xlabel('Batch')
    plt.ylabel('Accuracy (%)')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'training_progress.png'))
    plt.close()

def verify_training_targets(metrics):
    """Verify if training targets are met."""
    latest_accuracy = metrics['batch_accuracies'][-1] if metrics['batch_accuracies'] else 0
    latest_loss = metrics['batch_losses'][-1] if metrics['batch_losses'] else float('inf')
    
    # Calculate convergence rate
    if len(metrics['batch_losses']) > 10:
        recent_losses = metrics['batch_losses'][-10:]
        loss_change = (recent_losses[0] - recent_losses[-1]) / recent_losses[0]
        converging = loss_change > 0 and latest_loss < 1.0
    else:
        converging = False
    
    targets = {
        'accuracy': {
            'target': 91.7,
            'current': latest_accuracy,
            'met': latest_accuracy > 91.7
        },
        'convergence': {
            'target': 'Decreasing loss',
            'current': 'Converging' if converging else 'Not converging',
            'met': converging
        }
    }
    
    return targets

def main():
    """Main function to analyze training progress."""
    print("Analyzing training progress...")
    
    # Get latest training output
    output_file = 'training_output.txt'
    if not os.path.exists(output_file):
        print("No training output file found.")
        return
    
    # Parse and analyze metrics
    metrics = parse_training_output(output_file)
    
    # Plot progress
    plot_training_progress(metrics)
    
    # Verify targets
    targets = verify_training_targets(metrics)
    
    # Print results
    print("\nTraining Progress Summary:")
    print("-" * 50)
    for metric, data in targets.items():
        status = "✓" if data['met'] else "✗"
        print(f"{metric.title()}: {data['current']} (target: {data['target']}) {status}")
    print("-" * 50)
    
    if all(data['met'] for data in targets.values()):
        print("\nAll training targets have been met! ✓")
    else:
        print("\nSome targets are still not met. Training should continue.")

if __name__ == '__main__':
    main()
