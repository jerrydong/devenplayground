"""Implementation of the Domain Adaptation framework for cross-domain feature alignment."""

import torch
import torch.nn as nn
import torch.nn.functional as F

class FeatureAlignment(nn.Module):
    """Multi-scale feature alignment between radar and RGB domains"""
    def __init__(self, in_channels):
        super().__init__()
        self.alignment = nn.Sequential(
            nn.Conv2d(in_channels * 2, in_channels, 1),
            nn.BatchNorm2d(in_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels, in_channels, 3, padding=1),
            nn.BatchNorm2d(in_channels),
            nn.ReLU(inplace=True)
        )
        
    def forward(self, radar_feat, rgb_feat):
        # Ensure RGB features match radar feature dimensions
        if rgb_feat.shape != radar_feat.shape:
            rgb_feat = F.interpolate(rgb_feat, 
                                   size=radar_feat.shape[-2:],
                                   mode='bilinear',
                                   align_corners=False)
        # Concatenate and align features
        combined = torch.cat([radar_feat, rgb_feat], dim=1)
        return self.alignment(combined)

class SemanticMapper(nn.Module):
    """Maps features between radar and RGB domains"""
    def __init__(self, config):
        super().__init__()
        self.radar_to_rgb = nn.ModuleList([
            nn.Sequential(
                nn.Conv2d(dim, dim, 3, padding=1),
                nn.BatchNorm2d(dim),
                nn.ReLU(inplace=True),
                nn.Conv2d(dim, dim, 1)
            ) for dim in config.feature_dims
        ])
        self.rgb_to_radar = nn.ModuleList([
            nn.Sequential(
                nn.Conv2d(dim, dim, 3, padding=1),
                nn.BatchNorm2d(dim),
                nn.ReLU(inplace=True),
                nn.Conv2d(dim, dim, 1)
            ) for dim in config.feature_dims
        ])
        
    def forward(self, radar_features, rgb_features):
        # Bidirectional mapping
        radar_to_rgb = [map_layer(r_feat) 
                       for map_layer, r_feat in zip(self.radar_to_rgb, radar_features)]
        rgb_to_radar = [map_layer(v_feat)
                       for map_layer, v_feat in zip(self.rgb_to_radar, rgb_features)]
        return radar_to_rgb, rgb_to_radar

class MultiScaleDomainAdapter(nn.Module):
    """Multi-scale domain adaptation with feature alignment"""
    def __init__(self, config):
        super().__init__()
        self.feature_dims = config.feature_dims
        
        # Feature alignment at each scale
        self.aligners = nn.ModuleList([
            FeatureAlignment(dim) for dim in self.feature_dims
        ])
        
        # Semantic mapping between domains
        self.semantic_mapper = SemanticMapper(config)
        
        # Domain discriminators
        self.discriminators = nn.ModuleList([
            nn.Sequential(
                nn.Conv2d(dim, dim//2, 1),
                nn.ReLU(),
                nn.Conv2d(dim//2, 1, 1)
            ) for dim in self.feature_dims
        ])
        
    def compute_consistency_loss(self, radar_features, mapped_rgb, rgb_features, mapped_radar):
        """Compute cycle consistency loss for semantic mapping"""
        consistency_losses = []
        for r_feat, mr_feat, v_feat, mv_feat in zip(
            radar_features, mapped_radar, rgb_features, mapped_rgb):
            r_cons_loss = F.mse_loss(r_feat, mr_feat)
            v_cons_loss = F.mse_loss(v_feat, mv_feat)
            consistency_losses.append(r_cons_loss + v_cons_loss)
        return consistency_losses
    
    def forward(self, radar_features, rgb_features=None):
        """
        Args:
            radar_features: List of feature maps from radar domain
            rgb_features: Optional list of feature maps from RGB domain
        Returns:
            Features for classification or dict containing adaptation losses
        """
        if rgb_features is None:
            # UWB-only training mode
            # Concatenate all feature maps and pass through classifier
            features = torch.cat([f.mean([-2, -1]) for f in radar_features], dim=1)
            return self.classifier(features)
        
        # Full domain adaptation mode with RGB features
        # Feature alignment
        aligned_features = [aligner(r_feat, v_feat) 
                          for aligner, r_feat, v_feat 
                          in zip(self.aligners, radar_features, rgb_features)]
        
        # Semantic mapping
        mapped_rgb, mapped_radar = self.semantic_mapper(radar_features, rgb_features)
        
        # Consistency loss
        consistency_losses = self.compute_consistency_loss(
            radar_features, mapped_rgb, rgb_features, mapped_radar)
        
        # Domain adversarial loss
        domain_losses = []
        for disc, r_feat, v_feat in zip(self.discriminators, 
                                      aligned_features, rgb_features):
            radar_domain = disc(r_feat)
            video_domain = disc(v_feat)
            
            domain_loss = F.binary_cross_entropy_with_logits(
                radar_domain, torch.ones_like(radar_domain)
            ) + F.binary_cross_entropy_with_logits(
                video_domain, torch.zeros_like(video_domain)
            )
            domain_losses.append(domain_loss)
            
        return {
            'domain_losses': domain_losses,
            'consistency_losses': consistency_losses,
            'aligned_features': aligned_features,
            'mapped_rgb': mapped_rgb,
            'mapped_radar': mapped_radar
        }
