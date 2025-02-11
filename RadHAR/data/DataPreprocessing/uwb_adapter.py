"""
Ultra-wideband data adapter for RadHAR project.
Converts UWB range-Doppler images to point cloud format compatible with existing pipeline.
"""

import numpy as np
from PIL import Image

def extract_features(image):
    """
    Extract features from range-Doppler image.
    Args:
        image: np.array of shape (H, W, 3) containing range-Doppler image
    Returns:
        points: np.array of shape (N, 5) containing [x, y, z, velocity, intensity]
    """
    # Image dimensions map to physical space
    range_resolution = 0.1  # meters per pixel
    velocity_resolution = 0.1  # m/s per pixel
    
    # Create coordinate grids
    x_grid = np.linspace(0, image.shape[1] * range_resolution, image.shape[1])
    y_grid = np.linspace(-image.shape[0]/2 * velocity_resolution,
                        image.shape[0]/2 * velocity_resolution,
                        image.shape[0])
    X, Y = np.meshgrid(x_grid, y_grid)
    
    # Extract intensity from RGB
    intensity = np.mean(image, axis=2)
    
    # Create point cloud
    mask = intensity > np.mean(intensity)  # Only keep points above mean intensity
    points = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if mask[i, j]:
                x = X[i, j]  # Range
                y = Y[i, j]  # Velocity
                z = intensity[i, j] / np.max(intensity)  # Normalized height
                velocity = Y[i, j]  # Use Doppler velocity
                point_intensity = intensity[i, j]
                points.append([x, y, z, velocity, point_intensity])
    
    return np.array(points) if points else np.zeros((0, 5))

def convert_to_point_cloud(image_path):
    """
    Convert range-Doppler image to point cloud format.
    Args:
        image_path: Path to range-Doppler image file
    Returns:
        points: np.array of shape (N, 5) containing [x, y, z, velocity, intensity]
    """
    image = np.array(Image.open(image_path))
    return extract_features(image)

def preprocess_uwb_data(file_path):
    """
    Read and preprocess UWB data file to match format expected by voxels.py
    Args:
        file_path: Path to UWB data file (range-Doppler image)
    Returns:
        train_data: np.array of shape (num_samples, 60, 10, 32, 32)
                   60 frames per sample, 10x32x32 voxel grid
    """
    # Convert range-Doppler image to point cloud
    points = convert_to_point_cloud(file_path)
    if len(points) == 0:
        return np.array([])
    
    # Convert to voxel representation
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    velocity = points[:, 3]
    voxel = voxalize(10, 32, 32, x, y, z, velocity)
    
    return np.array([voxel])  # Single frame

def voxalize(x_points, y_points, z_points, x, y, z, velocity):
    """
    Create voxel representation of point cloud data.
    Args:
        x_points, y_points, z_points: Grid dimensions
        x, y, z: Point coordinates
        velocity: Point velocities
    Returns:
        pixel: Voxel grid of shape (x_points, y_points, z_points)
    """
    x_min = np.min(x)
    x_max = np.max(x)
    y_min = np.min(y)
    y_max = np.max(y)
    z_min = np.min(z)
    z_max = np.max(z)
    
    z_res = (z_max - z_min)/z_points if z_max > z_min else 1
    y_res = (y_max - y_min)/y_points if y_max > y_min else 1
    x_res = (x_max - x_min)/x_points if x_max > x_min else 1
    
    pixel = np.zeros([x_points, y_points, z_points])
    
    for i in range(len(x)):
        x_idx = min(int((x[i] - x_min) / x_res), x_points - 1)
        y_idx = min(int((y[i] - y_min) / y_res), y_points - 1)
        z_idx = min(int((z[i] - z_min) / z_res), z_points - 1)
        pixel[x_idx, y_idx, z_idx] += 1
    
    return pixel
