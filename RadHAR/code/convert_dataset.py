"""
Convert IURHA2023 UWB dataset to RadHAR format.
Maps actions and converts range-Doppler images to point cloud format.
"""

import os
import numpy as np
from tqdm import tqdm
from PIL import Image
import sys

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from data.DataPreprocessing.uwb_adapter import convert_to_point_cloud

def convert_dataset(src_dir, dst_dir):
    """Convert IURHA2023 dataset to RadHAR format
    Args:
        src_dir: Source directory containing IURHA2023 dataset
        dst_dir: Destination directory for RadHAR format data
    """
    # Map actions to RadHAR format
    action_map = {
        'boxing': 'boxing',
        'jump_up': 'jump',
        'squat_and_stand': 'squats',
        'walk_in_place': 'walk'
    }
    
    # Create destination directory
    os.makedirs(dst_dir, exist_ok=True)
    
    # Process each action type
    for action in tqdm(os.listdir(src_dir), desc='Converting actions'):
        action_base = action.split('_')[0]
        if action_base not in action_map:
            continue
        
        # Map to RadHAR action name
        radhar_action = action_map[action_base]
        src_path = os.path.join(src_dir, action)
        dst_path = os.path.join(dst_dir, radhar_action)
        os.makedirs(dst_path, exist_ok=True)
        
        # Convert each sequence
        if os.path.isdir(src_path):
            for file_name in tqdm(os.listdir(src_path), desc=f'Converting {action}'):
                if file_name.endswith('.jpg'):
                    try:
                        # Convert range-Doppler image to point cloud
                        src_file = os.path.join(src_path, file_name)
                        points = convert_to_point_cloud(src_file)
                        
                        # Save as numpy array
                        dst_file = os.path.join(dst_path, file_name.replace('.jpg', '.npy'))
                        np.save(dst_file, points)
                    except Exception as e:
                        print(f"Error converting {file_name}: {str(e)}")
                        continue

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Convert IURHA2023 dataset to RadHAR format')
    parser.add_argument('--src_dir', required=True,
                      help='Source directory containing IURHA2023 dataset')
    parser.add_argument('--dst_dir', required=True,
                      help='Destination directory for RadHAR format data')
    args = parser.parse_args()
    
    try:
        convert_dataset(args.src_dir, args.dst_dir)
        print("Dataset conversion completed successfully")
    except Exception as e:
        print(f"Error converting dataset: {str(e)}")
        raise
