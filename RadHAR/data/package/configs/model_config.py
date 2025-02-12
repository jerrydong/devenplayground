"""Configuration file for model architecture and training parameters."""

class Config:
    # Data parameters for LIARA dataset
    input_channels = 3  # 3 UWB radars
    range_bins = 184   # Range dimension size
    frames_per_window = 50  # Time dimension (1 second at 50 fps)
    num_classes = 14   # Number of activities in LIARA dataset
    
    # ViT parameters optimized for radar data
    patch_size = 8     # Smaller patches for fine-grained features
    hidden_dim = 512   # Reduced from 768 to match data scale
    num_heads = 8      # Adjusted for hidden_dim
    num_layers = 8     # Reduced complexity
    mlp_dim = 2048    # Adjusted for hidden_dim
    dropout = 0.2     # Increased for better regularization
    
    # Hierarchical Attention parameters
    attention_levels = 3  # Number of levels in hierarchical attention
    feature_dims = [64, 128, 256]  # Feature dimensions at each level
    
    # Domain Adaptation parameters
    domain_adaptation_weight = 0.1
    feature_matching_weight = 0.5
    
    # Training parameters
    batch_size = 32
    learning_rate = 1e-4
    num_epochs = 100
    weight_decay = 1e-4
    data_dir = 'data/converted_dataset'  # Base directory for converted dataset
