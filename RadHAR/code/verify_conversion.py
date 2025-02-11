"""
Verify UWB data conversion to RadHAR format.
Tests sample data conversion and validates output format.
"""

import os
import sys
import numpy as np
import shutil
from PIL import Image

def setup_test_data():
    """Set up test directories and copy sample data"""
    # Get absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    # Create test directories
    test_input = os.path.join(project_root, 'test_data/input/boxing_Person1')
    test_output = os.path.join(project_root, 'test_data/output')
    os.makedirs(test_input, exist_ok=True)
    os.makedirs(test_output, exist_ok=True)
    
    # Create sample test data
    test_image = np.zeros((280, 280, 3), dtype=np.uint8)
    test_image[140:180, 100:200] = 255  # Create a simple pattern
    dst_file = os.path.join(test_input, 'c9p1n1.jpg')
    Image.fromarray(test_image).save(dst_file)
    
    return test_input, test_output

def verify_voxel_dimensions(data):
    """Verify voxel grid dimensions"""
    # Check shape (B, 10, 32, 32) for voxel grid, where B is batch size
    if len(data.shape) != 4 or data.shape[1:] != (10, 32, 32):
        raise ValueError(f"Invalid voxel grid shape: {data.shape}, expected (B, 10, 32, 32)")
    
    print("\nVoxel grid verification:")
    print(f"Shape: {data.shape}")
    print(f"Value range: {np.min(data):.3f} to {np.max(data):.3f}")
    return True

def verify_visualization(data, action_type='boxing'):
    """Verify visualization types"""
    from doppler_visualization import plot_point_cloud, plot_3d_doppler
    
    # Test point cloud visualization
    plot_point_cloud(data, action_type, data_type='uwb', save_path='test_point_cloud.png')
    
    # Test Doppler visualization
    f = np.linspace(0, 100, data.shape[0])
    t = np.linspace(0, 1, data.shape[1])
    plot_3d_doppler(f, t, data, action_type, data_type='uwb', save_path='test_doppler.png')
    
    print("\nVisualization verification:")
    print("Generated test_point_cloud.png and test_doppler.png")
    return True

def verify_point_cloud(data):
    """Verify point cloud format and dimensions"""
    # Check shape (N, 5) for x,y,z,velocity,intensity
    if len(data.shape) != 2 or data.shape[1] != 5:
        raise ValueError(f"Invalid point cloud shape: {data.shape}, expected (N, 5)")
    
    # Check value ranges
    if np.any(np.isinf(data)) or np.any(np.isnan(data)):
        raise ValueError("Point cloud contains inf/nan values")
    
    print("Point cloud format verification:")
    print(f"Shape: {data.shape}")
    print(f"Fields: x,y,z,velocity,intensity")
    print(f"Value range: {np.min(data):.3f} to {np.max(data):.3f}")
    return True

def verify_conversion():
    """Run conversion verification"""
    print("Starting verification suite...")
    
    # Set up test data
    test_input, test_output = setup_test_data()
    print("\nTest data setup complete")
    
    # Run conversion script
    from convert_dataset import convert_dataset
    convert_dataset(os.path.dirname(test_input), test_output)
    print("\nData conversion complete")
    
    # Load and verify output
    output_file = os.path.join(test_output, 'boxing/c9p1n1.npy')
    if not os.path.exists(output_file):
        raise FileNotFoundError(f"Conversion failed: {output_file} not found")
    
    # Load converted data
    point_cloud = np.load(output_file)
    
    # Run verification suite
    verify_point_cloud(point_cloud)  # Verify point cloud format
    
    # Convert to voxel grid and verify dimensions
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    sys.path.append(project_root)
    
    from data.DataPreprocessing.uwb_adapter import preprocess_uwb_data
    voxel_data = preprocess_uwb_data(os.path.join(test_input, 'c9p1n1.jpg'))
    verify_voxel_dimensions(voxel_data)  # Verify voxel grid dimensions
    
    # Verify visualizations
    verify_visualization(point_cloud)  # Verify visualization types
    
    print("\nAll verification steps completed successfully")

if __name__ == '__main__':
    try:
        verify_conversion()
    except Exception as e:
        print(f"Verification failed: {str(e)}")
        raise
