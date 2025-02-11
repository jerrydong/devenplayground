import matplotlib
matplotlib.use('Agg')  # Set backend to Agg (no GUI needed)

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting
import os
import pandas as pd
from scipy import signal
import yaml
import re
from PIL import Image  # Required for loading UWB images

# Configure matplotlib for 3D plotting
plt.rcParams['axes.formatter.useoffset'] = False
plt.rcParams['axes.grid'] = True

# Enable 3D plotting
from mpl_toolkits.mplot3d import proj3d, art3d

def load_radar_data(file_path):
    """Load radar data file and extract point cloud information"""
    points = []
    current_point = {}
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if line == '---':
            if current_point:
                points.append(current_point)
                current_point = {}
        elif ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            if value:  # 如果值不为空
                try:
                    value = float(value)
                    current_point[key] = value
                except ValueError:
                    pass
    
    # Extract x, y, z coordinates and intensity values
    x = [p.get('x', 0) for p in points if 'x' in p]
    y = [p.get('y', 0) for p in points if 'y' in p]
    z = [p.get('z', 0) for p in points if 'z' in p]
    intensities = [p.get('intensity', 0) for p in points if 'intensity' in p]
    
    # Convert to numpy array
    return np.array([x, y, z, intensities]).T

def preprocess_data(raw_data):
    """Preprocess radar data
    1. Remove outliers
    2. Normalize data
    3. Denoise signal
    """
    # Separate coordinates and intensity data
    coords = raw_data[:, :3]
    intensities = raw_data[:, 3]
    
    # Process coordinate data
    coords_processed = np.clip(coords, np.percentile(coords, 1), np.percentile(coords, 99))
    coords_processed = (coords_processed - np.mean(coords_processed, axis=0)) / np.std(coords_processed, axis=0)
    
    # Process intensity data
    intensities_processed = np.clip(intensities, np.percentile(intensities, 1), np.percentile(intensities, 99))
    intensities_processed = (intensities_processed - np.mean(intensities_processed)) / np.std(intensities_processed)
    
    return np.column_stack((coords_processed, intensities_processed))

def generate_doppler_spectrogram(data, fs=100, nperseg=64):
    """Generate Doppler spectrogram using intensity values"""
    intensities = data[:, 3]  # 使用强度值
    f, t, Sxx = signal.spectrogram(intensities, fs=fs, nperseg=nperseg)
    return f, t, Sxx

def plot_3d_doppler(f, t, Sxx, action_type, data_type='mmwave', save_path=None):
    """Plot 3D Doppler spectrogram"""
    if data_type == 'uwb':
        # For UWB data, plot range-Doppler image directly
        plt.figure(figsize=(12, 8))
        plt.imshow(Sxx, aspect='auto', origin='lower', cmap='jet')
        plt.colorbar(label='Power (dB)')
        plt.xlabel('Time (s)')
        plt.ylabel('Range (m)')
        plt.title(f'Action Type: {action_type} - Range-Doppler Image (UWB)')
    else:
        # For mmWave data, plot 3D spectrogram
        fig = plt.figure(figsize=(12, 8))
        # Create 3D axes
        ax = Axes3D(fig)  # Create Axes3D instance directly
        
        # Create grid
        T, F = np.meshgrid(t, f)
        
        # Plot 3D surface with log scale
        Z = 10 * np.log10(Sxx + 1e-10)
        surf = ax.plot_surface(T, F, Z, cmap='jet')  # Remove rstride/cstride
        
        # Set labels and title
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Frequency (Hz)')
        ax.set_zlabel('Power/Frequency (dB/Hz)')
        ax.set_title(f'Action Type: {action_type} - 3D Doppler Spectrogram (mmWave)')
        
        # Add colorbar
        fig.colorbar(surf, ax=ax, label='Power (dB)')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def plot_point_cloud(data, action_type, data_type='mmwave', save_path=None):
    """Plot point cloud visualization"""
    fig = plt.figure(figsize=(12, 8))
    # Create 3D axes
    ax = Axes3D(fig)  # Create Axes3D instance directly
    
    # Use intensity values for color
    point_size = 10 if data_type=='mmwave' else 5
    scatter = ax.scatter(data[:, 0], data[:, 1], data[:, 2], 
                        c=data[:, 3], cmap='jet', 
                        s=point_size)  # Use scalar point size
    
    # Set labels and title
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title(f'Action Type: {action_type} - Point Cloud ({data_type})')
    
    # Add colorbar
    fig.colorbar(scatter, ax=ax, label='Signal Intensity')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def process_all_actions(data_dir, output_dir, data_type='mmwave'):
    """Process all action data and generate visualizations
    Args:
        data_dir: Directory containing action data
        output_dir: Directory to save visualizations
        data_type: 'mmwave' or 'uwb'
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Process all action types
    for action_type in os.listdir(data_dir):
        action_path = os.path.join(data_dir, action_type)
        if os.path.isdir(action_path):
            # Create output directory for each action type
            action_output_dir = os.path.join(output_dir, action_type)
            os.makedirs(action_output_dir, exist_ok=True)
            
            # Process samples for this action type
            file_ext = '.jpg' if data_type == 'uwb' else '.txt'
            for file_name in os.listdir(action_path)[:5]:  # Process first 5 samples
                if file_name.endswith(file_ext):
                    print(f'Processing file: {file_name}')
                    
                    file_path = os.path.join(action_path, file_name)
                    if data_type == 'uwb':
                        # For UWB data, load image directly
                        image = np.array(Image.open(file_path))
                        processed_data = image  # Range-Doppler image is already preprocessed
                        
                        # Save range-Doppler visualization
                        save_path_doppler = os.path.join(action_output_dir, f'{file_name[:-4]}_doppler.png')
                        plot_3d_doppler(None, None, processed_data, action_type, data_type='uwb', save_path=save_path_doppler)
                        
                        # Convert to point cloud and save visualization
                        from ..data.DataPreprocessing.uwb_adapter import convert_to_point_cloud
                        points = convert_to_point_cloud(file_path)
                        save_path_cloud = os.path.join(action_output_dir, f'{file_name[:-4]}_cloud.png')
                        plot_point_cloud(points, action_type, data_type='uwb', save_path=save_path_cloud)
                    else:
                        # For mmWave data, use existing pipeline
                        raw_data = load_radar_data(file_path)
                        processed_data = preprocess_data(raw_data)
                        
                        # Generate and save point cloud visualization
                        save_path_cloud = os.path.join(action_output_dir, f'{file_name[:-4]}_cloud.png')
                        plot_point_cloud(processed_data, action_type, data_type='mmwave', save_path=save_path_cloud)
                        
                        # Generate and save Doppler spectrogram
                        f, t, Sxx = generate_doppler_spectrogram(processed_data)
                        save_path_doppler = os.path.join(action_output_dir, f'{file_name[:-4]}_doppler.png')
                        plot_3d_doppler(f, t, Sxx, action_type, data_type='mmwave', save_path=save_path_doppler)
                    
                    print(f'Completed: {file_name}')

def get_uwb_adapter():
    """Import UWB adapter module safely"""
    import os
    import sys
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)
    from data.DataPreprocessing.uwb_adapter import convert_to_point_cloud
    return convert_to_point_cloud

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Generate visualizations for radar data')
    parser.add_argument('--data_dir', default="../data/Data/Train",
                      help='Training data directory')
    parser.add_argument('--output_dir', default="../visualizations/doppler_images",
                      help='Output directory')
    parser.add_argument('--data_type', default='mmwave', choices=['mmwave', 'uwb'],
                      help='Type of radar data (mmwave or uwb)')
    args = parser.parse_args()
    
    try:
        if args.data_type == 'uwb':
            # Test UWB adapter import
            get_uwb_adapter()
        process_all_actions(args.data_dir, args.output_dir, args.data_type)
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        raise
