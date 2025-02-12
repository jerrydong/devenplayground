import os
import json

def analyze_radar_data():
    base_path = "B524/datasets/RadHAR/RadHAR-master/Data/Train"
    action_types = os.listdir(base_path)
    
    analysis = {
        'action_types': action_types,
        'samples_per_action': {},
        'data_format': {}
    }
    
    total_samples = 0
    for action in action_types:
        action_path = os.path.join(base_path, action)
        files = os.listdir(action_path)
        num_samples = len(files)
        total_samples += num_samples
        analysis['samples_per_action'][action] = num_samples
        
        # Analyze first file for data format
        first_file = os.path.join(action_path, files[0])
        with open(first_file, 'r') as f:
            data = f.readlines()[:10]  # Read first 10 lines for format analysis
            analysis['data_format'][action] = {
                'file_size_bytes': os.path.getsize(first_file),
                'sample_lines': len(data),
                'format_preview': ''.join(data)
            }
    
    print('\n=== RadHAR Dataset Analysis ===')
    print(f'\nTotal number of action types: {len(action_types)}')
    print(f'Action types: {action_types}')
    print(f'\nTotal samples across all actions: {total_samples}')
    print('\nSamples per Action Type:')
    for action, count in analysis['samples_per_action'].items():
        print(f'- {action}: {count} samples')
    print('\nData Format Analysis:')
    for action, info in analysis['data_format'].items():
        print(f'\n{action.upper()} FORMAT:')
        print(f'- File size: {info["file_size_bytes"]/1024:.2f} KB')
        print(f'- Sample preview:\n{info["format_preview"]}')

if __name__ == "__main__":
    analyze_radar_data()
