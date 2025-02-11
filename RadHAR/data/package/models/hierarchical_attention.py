"""Implementation of the Hierarchical Attention mechanism for UWB radar action recognition."""

import torch
import torch.nn as nn
import torch.nn.functional as F

class RangeTimeAttention(nn.Module):
    """Attention module for range-time features"""
    def __init__(self, in_channels):
        super().__init__()
        self.range_attn = nn.Sequential(
            nn.Conv2d(in_channels, in_channels//2, 1),
            nn.ReLU(),
            nn.Conv2d(in_channels//2, 1, 1),
            nn.Sigmoid()
        )
        self.time_attn = nn.Sequential(
            nn.Conv2d(in_channels, in_channels//2, 1),
            nn.ReLU(),
            nn.Conv2d(in_channels//2, 1, 1),
            nn.Sigmoid()
        )
        
    def forward(self, x):
        # x shape: (batch, channels, range_bins, frames)
        range_weights = self.range_attn(x)  # Focus on important ranges
        time_weights = self.time_attn(x)    # Focus on important time steps
        return x * range_weights * time_weights

class MultiLevelFeatureRecalibration(nn.Module):
    """Multi-level feature recalibration for radar signals"""
    def __init__(self, in_channels, reduction_ratio=16):
        super().__init__()
        self.range_time_attn = RangeTimeAttention(in_channels)
        self.channel_attn = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Conv2d(in_channels, in_channels//reduction_ratio, 1),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels//reduction_ratio, in_channels, 1),
            nn.Sigmoid()
        )
        
    def forward(self, x):
        # Apply range-time attention
        x = self.range_time_attn(x)
        # Apply channel attention
        y = self.channel_attn(x)
        return x * y

class RadarFeaturePyramid(nn.Module):
    """Feature pyramid for multi-scale feature extraction"""
    def __init__(self, config):
        super().__init__()
        self.conv_layers = nn.ModuleList([
            nn.Sequential(
                nn.Conv2d(config.input_channels if i == 0 else config.feature_dims[i-1],
                         config.feature_dims[i],
                         kernel_size=3,
                         stride=2 if i > 0 else 1,
                         padding=1),
                nn.BatchNorm2d(config.feature_dims[i]),
                nn.ReLU(inplace=True)
            ) for i in range(config.attention_levels)
        ])
        
    def forward(self, x):
        features = []
        for conv in self.conv_layers:
            x = conv(x)
            features.append(x)
        return features

class HierarchicalAttention(nn.Module):
    """Hierarchical attention for UWB radar action recognition"""
    def __init__(self, config):
        super().__init__()
        self.feature_pyramid = RadarFeaturePyramid(config)
        self.attention_modules = nn.ModuleList([
            MultiLevelFeatureRecalibration(dim)
            for dim in config.feature_dims
        ])
        
        # Fusion layers
        self.fusion_convs = nn.ModuleList([
            nn.Conv2d(dim1 + dim2, dim1, 1)
            for dim1, dim2 in zip(config.feature_dims[:-1], config.feature_dims[1:])
        ])
        
    def forward(self, x):
        """
        Args:
            x: Radar data of shape (batch, channels, range_bins, range_bins, frames)
        Returns:
            List of recalibrated feature maps at different scales
        """
        # Reshape input: [batch, channels, range_bins, range_bins, frames] -> [batch, channels, range_bins, range_bins * frames]
        batch_size, channels, h, w, frames = x.shape
        x = x.reshape(batch_size, channels, h, w * frames)
        
        # Extract multi-scale features
        features = self.feature_pyramid(x)
        
        # Apply attention at each level
        attended_features = [attn(feat) for attn, feat in zip(self.attention_modules, features)]
        
        # Feature fusion (from top to bottom)
        for i in range(len(attended_features)-2, -1, -1):
            # Upsample higher level features
            higher_feat = F.interpolate(attended_features[i+1], 
                                     size=attended_features[i].shape[-2:],
                                     mode='bilinear',
                                     align_corners=False)
            # Concatenate and fuse
            concat_feat = torch.cat([attended_features[i], higher_feat], dim=1)
            attended_features[i] = self.fusion_convs[i](concat_feat)
            
        return attended_features
