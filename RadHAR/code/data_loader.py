"""Data loading pipeline for RadHAR UWB action recognition."""

import os
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image

from data.DataPreprocessing.uwb_adapter import preprocess_uwb_data, convert_to_point_cloud
from data.package.configs.model_config import Config

class RadarDataset(Dataset):
    """Dataset class for UWB radar data."""
    def __init__(self, data_dir, transform=None, is_training=True, samples=None):
        self.data_dir = data_dir
        self.transform = transform
        self.is_training = is_training
        self.samples = []
        self.action_to_idx = {}
        
        if samples is not None:
            self.init_from_samples(samples)
        else:
            self.preprocess_data()
    
    def init_from_samples(self, samples):
        """Initialize dataset from pre-split samples list."""
        # Create action to index mapping from provided samples
        actions = sorted(list(set(action for _, action in samples)))
        self.action_to_idx = {action: idx for idx, action in enumerate(actions)}
        
        # Store samples
        self.samples = [
            {
                'path': path,
                'action': action,
                'label': self.action_to_idx[action]
            }
            for path, action in samples
        ]
    
    def preprocess_data(self):
        """Load and preprocess all data samples."""
        # Create action to index mapping
        actions = sorted(os.listdir(self.data_dir))
        self.action_to_idx = {action: idx for idx, action in enumerate(actions)}
        
        # Load all samples
        for action in actions:
            action_path = os.path.join(self.data_dir, action)
            if os.path.isdir(action_path):
                for sample in os.listdir(action_path):
                    if sample.endswith('.jpg'):
                        self.samples.append({
                            'path': os.path.join(action_path, sample),
                            'action': action,
                            'label': self.action_to_idx[action]
                        })
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        """Get a single sample."""
        sample = self.samples[idx]
        
        # Load and preprocess UWB data
        data = preprocess_uwb_data(sample['path'])
        
        # Convert to tensor
        data = torch.FloatTensor(data)
        
        # Apply transforms if any
        if self.transform is not None:
            data = self.transform(data)
        
        return data, sample['label']

class RadarDataAugmentation:
    """Data augmentation for UWB radar data."""
    def __init__(self, config):
        self.config = config
    
    def get_train_transform(self):
        """Get training data transforms."""
        return transforms.Compose([
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(10),
            transforms.Normalize(mean=[0.5], std=[0.5])
        ])
    
    def get_val_transform(self):
        """Get validation data transforms."""
        return transforms.Compose([
            transforms.Normalize(mean=[0.5], std=[0.5])
        ])

def create_dataloaders(config):
    """Create training and validation dataloaders."""
    # Setup data augmentation
    augmentation = RadarDataAugmentation(config)
    
    # Create datasets with train/val split from Train directory
    train_dir = os.path.join(config.data_dir, 'Train')
    all_samples = []
    for action in os.listdir(train_dir):
        action_path = os.path.join(train_dir, action)
        if os.path.isdir(action_path):
            samples = [os.path.join(action_path, f) for f in os.listdir(action_path) if f.endswith('.jpg')]
            all_samples.extend([(s, action) for s in samples])
    
    # Random split 80/20
    np.random.seed(42)
    np.random.shuffle(all_samples)
    split_idx = int(len(all_samples) * 0.8)
    
    train_samples = all_samples[:split_idx]
    val_samples = all_samples[split_idx:]
    
    # Create datasets
    train_dataset = RadarDataset(
        train_dir,
        transform=augmentation.get_train_transform(),
        is_training=True,
        samples=train_samples
    )
    
    val_dataset = RadarDataset(
        train_dir,
        transform=augmentation.get_val_transform(),
        is_training=False,
        samples=val_samples
    )
    
    # Create dataloaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=config.batch_size,
        shuffle=True,
        num_workers=4,
        pin_memory=True
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=config.batch_size,
        shuffle=False,
        num_workers=4,
        pin_memory=True
    )
    
    return train_loader, val_loader

def verify_data_dimensions(loader):
    """Verify data dimensions match requirements."""
    for batch, _ in loader:
        print("Batch shape:", batch.shape)
        # Expected shape: (batch_size, 60, 10, 32, 32)
        assert batch.ndim == 5, f"Expected 5D tensor, got {batch.ndim}D"
        assert batch.shape[1] == 60, f"Expected 60 frames, got {batch.shape[1]}"
        assert batch.shape[2:] == (10, 32, 32), f"Expected (10, 32, 32) voxel grid, got {batch.shape[2:]}"
        break
    print("Data dimensions verified successfully")

if __name__ == '__main__':
    # Test data loading pipeline
    config = Config()
    train_loader, val_loader = create_dataloaders(config)
    verify_data_dimensions(train_loader)
