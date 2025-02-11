"""Main training script for RadHAR UWB action recognition."""

import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import numpy as np
from tqdm import tqdm

# Import local modules
from data.package.models.hierarchical_attention import HierarchicalAttention
from data.package.models.domain_adaptation import MultiScaleDomainAdapter
from data.package.configs.model_config import Config

class CheckpointManager:
    """Manages model checkpoints and training state."""
    def __init__(self, save_dir='checkpoints'):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
        
    def save_checkpoint(self, state, filename):
        """Save model and training state."""
        path = os.path.join(self.save_dir, filename)
        torch.save(state, path)
        
    def load_checkpoint(self, filename):
        """Load model and training state."""
        path = os.path.join(self.save_dir, filename)
        return torch.load(path)

class Trainer:
    """Handles model training and evaluation."""
    def __init__(self, config, device='cuda'):
        self.config = config
        self.device = device
        
        # Initialize models
        self.model = HierarchicalAttention(config).to(device)
        self.domain_adapter = MultiScaleDomainAdapter(config).to(device)
        
        # Setup optimizers
        self.optimizer = optim.Adam([
            {'params': self.model.parameters()},
            {'params': self.domain_adapter.parameters()}
        ], lr=config.learning_rate, weight_decay=config.weight_decay)
        
        # Setup loss functions
        self.criterion = nn.CrossEntropyLoss()
        
        # Setup checkpoint manager
        self.checkpoint_manager = CheckpointManager()
        
        # Initialize metrics
        self.metrics = {
            'train_loss': [],
            'val_loss': [],
            'accuracy': [],
            'domain_score': []
        }
    
    def train_epoch(self, train_loader):
        """Train for one epoch."""
        self.model.train()
        self.domain_adapter.train()
        
        total_loss = 0
        correct = 0
        total = 0
        
        for batch_idx, (data, target) in enumerate(tqdm(train_loader)):
            data, target = data.to(self.device), target.to(self.device)
            
            # Forward pass
            self.optimizer.zero_grad()
            features = self.model(data)
            domain_features = self.domain_adapter(features)
            
            # Calculate losses
            task_loss = self.criterion(domain_features, target)
            domain_loss = self.domain_adapter.compute_loss()
            total_batch_loss = task_loss + self.config.domain_adaptation_weight * domain_loss
            
            # Backward pass
            total_batch_loss.backward()
            self.optimizer.step()
            
            # Update metrics
            total_loss += total_batch_loss.item()
            pred = domain_features.argmax(dim=1)
            correct += pred.eq(target).sum().item()
            total += target.size(0)
            
            # Update progress
            if batch_idx % 10 == 0:
                print(f'Train Batch [{batch_idx}/{len(train_loader)}] '
                      f'Loss: {total_batch_loss.item():.4f} '
                      f'Acc: {100.*correct/total:.2f}%')
        
        epoch_loss = total_loss / len(train_loader)
        epoch_acc = 100. * correct / total
        
        return epoch_loss, epoch_acc
    
    def validate(self, val_loader):
        """Evaluate on validation set."""
        self.model.eval()
        self.domain_adapter.eval()
        
        val_loss = 0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for data, target in val_loader:
                data, target = data.to(self.device), target.to(self.device)
                
                # Forward pass
                features = self.model(data)
                domain_features = self.domain_adapter(features)
                
                # Calculate loss
                loss = self.criterion(domain_features, target)
                val_loss += loss.item()
                
                # Calculate accuracy
                pred = domain_features.argmax(dim=1)
                correct += pred.eq(target).sum().item()
                total += target.size(0)
        
        val_loss /= len(val_loader)
        val_acc = 100. * correct / total
        
        return val_loss, val_acc
    
    def train(self, train_loader, val_loader, num_epochs=None):
        """Full training loop."""
        if num_epochs is None:
            num_epochs = self.config.num_epochs
            
        best_acc = 0
        
        for epoch in range(num_epochs):
            print(f'\nEpoch {epoch+1}/{num_epochs}')
            
            # Train and validate
            train_loss, train_acc = self.train_epoch(train_loader)
            val_loss, val_acc = self.validate(val_loader)
            domain_score = self.domain_adapter.compute_alignment_score()
            
            # Update metrics
            self.metrics['train_loss'].append(train_loss)
            self.metrics['val_loss'].append(val_loss)
            self.metrics['accuracy'].append(val_acc)
            self.metrics['domain_score'].append(domain_score)
            
            # Save best model
            if val_acc > best_acc:
                best_acc = val_acc
                self.save_checkpoint('best_model.pth')
            
            # Save periodic checkpoint
            if (epoch + 1) % 10 == 0:
                self.save_checkpoint(f'checkpoint_epoch_{epoch+1}.pth')
            
            print(f'Train Loss: {train_loss:.4f} Train Acc: {train_acc:.2f}%')
            print(f'Val Loss: {val_loss:.4f} Val Acc: {val_acc:.2f}%')
            print(f'Domain Score: {domain_score:.4f}')
    
    def save_checkpoint(self, filename):
        """Save training checkpoint."""
        state = {
            'model_state_dict': self.model.state_dict(),
            'domain_adapter_state_dict': self.domain_adapter.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'metrics': self.metrics,
            'config': self.config
        }
        self.checkpoint_manager.save_checkpoint(state, filename)
    
    def load_checkpoint(self, filename):
        """Load training checkpoint."""
        state = self.checkpoint_manager.load_checkpoint(filename)
        self.model.load_state_dict(state['model_state_dict'])
        self.domain_adapter.load_state_dict(state['domain_adapter_state_dict'])
        self.optimizer.load_state_dict(state['optimizer_state_dict'])
        self.metrics = state['metrics']

def main():
    """Main training function."""
    # Load configuration
    config = Config()
    
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using device: {device}')
    
    # Initialize trainer
    trainer = Trainer(config, device)
    
    # TODO: Initialize data loaders
    # This will be implemented in the data loading pipeline
    train_loader = None
    val_loader = None
    
    # Start training
    trainer.train(train_loader, val_loader)

if __name__ == '__main__':
    main()
