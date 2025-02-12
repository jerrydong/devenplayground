"""
Analyze performance results for UWB data conversion and processing.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def get_uwb_modules():
    """Import UWB modules safely"""
    import os
    import sys
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)
    try:
        from data.DataPreprocessing.uwb_adapter import convert_to_point_cloud, preprocess_uwb_data
        return convert_to_point_cloud, preprocess_uwb_data
    except ImportError as e:
        print(f"Error importing UWB modules: {str(e)}")
        return None, None

def analyze_point_cloud_format(data_dir):
    """Analyze point cloud format and dimensions"""
    results = {}
    total_points = 0
    num_samples = 0
    expected_shape = (4002, 5)  # Expected point cloud dimensions
    
    # Import UWB adapter
    convert_to_point_cloud, _ = get_uwb_modules()
    if not convert_to_point_cloud:
        print("Failed to import UWB modules")
        return None
    
    print("\nPoint Cloud Format Analysis:")
    for action in os.listdir(data_dir):
        action_dir = os.path.join(data_dir, action)
        if os.path.isdir(action_dir):
            action_points = []
            for sample in os.listdir(action_dir):
                if sample.endswith('.jpg'):
                    sample_path = os.path.join(action_dir, sample)
                    try:
                        # Convert UWB data to point cloud
                        data = convert_to_point_cloud(sample_path)
                        if data is not None and data.size > 0:
                            action_points.append(data.shape)
                            total_points += data.shape[0]
                            num_samples += 1
                            
                            # Verify dimensions
                            if data.shape == expected_shape:
                                print(f"✓ Point cloud format verified for {sample}: {data.shape}")
                            else:
                                print(f"✗ Incorrect point cloud format for {sample}: {data.shape}, expected {expected_shape}")
                    except Exception as e:
                        print(f"Error processing {sample}: {str(e)}")
                        continue
            
            if action_points:
                results[action] = {
                    'avg_points': np.mean([shape[0] for shape in action_points]),
                    'std_points': np.std([shape[0] for shape in action_points]),
                    'num_features': action_points[0][1]
                }
    
    print("\nPoint Cloud Format Analysis:")
    if num_samples > 0:
        print(f"Average points per sample: {total_points/num_samples:.2f}")
        if results:
            print(f"Number of features: {results[list(results.keys())[0]]['num_features']}")
            print("\nPoints per action type:")
            for action, stats in results.items():
                print(f"{action}: {stats['avg_points']:.2f} ± {stats['std_points']:.2f} points")
    else:
        print("No samples processed")
    
    return results

def analyze_voxel_dimensions(data_dir):
    """Analyze voxel grid dimensions"""
    # Import UWB adapter
    _, preprocess_uwb_data = get_uwb_modules()
    if not preprocess_uwb_data:
        print("Failed to import UWB modules")
        return []
    
    voxel_shapes = []
    total_samples = 0
    expected_shape = (1, 10, 32, 32)
    
    print("\nVoxel Grid Analysis:")
    print(f"Expected dimensions: {expected_shape}")
    
    correct_samples = 0
    total_processed = 0
    
    # Track results by action type
    action_results = {}
    
    for action in os.listdir(data_dir):
        action_dir = os.path.join(data_dir, action)
        if os.path.isdir(action_dir):
            for sample in os.listdir(action_dir):
                if sample.endswith('.jpg'):
                    sample_path = os.path.join(action_dir, sample)
                    try:
                        voxel_data = preprocess_uwb_data(sample_path)
                        if voxel_data.size > 0:
                            voxel_shapes.append(voxel_data.shape)
                            total_samples += 1
                    except Exception as e:
                        print(f"Error processing {sample}: {str(e)}")
    
    print("\nVoxel Grid Analysis:")
    if voxel_shapes:
        shape = voxel_shapes[0]
        print(f"Voxel grid dimensions: {shape}")
        print(f"Expected dimensions: {expected_shape}")
        print("Dimensions verified:", shape == expected_shape)
        print(f"Total samples processed: {total_samples}")
        print(f"Samples with correct dimensions: {sum(1 for s in voxel_shapes if s == expected_shape)}")
    else:
        print("No voxel data found")
    
    return voxel_shapes

def analyze_data_distribution(data_dir):
    """Analyze data distribution across actions"""
    action_counts = {}
    for action in os.listdir(data_dir):
        action_dir = os.path.join(data_dir, action)
        if os.path.isdir(action_dir):
            action_counts[action] = len([f for f in os.listdir(action_dir) if f.endswith('.jpg')])
    
    print("\nData Distribution Analysis:")
    print("Samples per action:")
    for action, count in action_counts.items():
        print(f"{action}: {count} samples")
    
    return action_counts

def main():
    data_dir = "../data/Data/Train"
    
    # Analyze point cloud format
    point_cloud_stats = analyze_point_cloud_format(data_dir)
    
    # Analyze voxel dimensions
    voxel_shapes = analyze_voxel_dimensions(data_dir)
    
    # Analyze data distribution
    action_counts = analyze_data_distribution(data_dir)
    
    # Plot data distribution
    plt.figure(figsize=(10, 6))
    plt.bar(action_counts.keys(), action_counts.values())
    plt.title('Data Distribution Across Actions')
    plt.xlabel('Action Type')
    plt.ylabel('Number of Samples')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('../visualizations/uwb_results/summary/data_distribution.png')
    plt.close()

if __name__ == '__main__':
    main()
