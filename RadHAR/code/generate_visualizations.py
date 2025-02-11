import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
from matplotlib.text import Text
from PIL import Image

def get_uwb_adapter():
    """Import UWB adapter module safely"""
    import os
    import sys
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(os.path.dirname(current_dir))
    sys.path.append(parent_dir)
    from data.DataPreprocessing.uwb_adapter import convert_to_point_cloud
    return convert_to_point_cloud

# Configure plotting style
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3
plt.rcParams['grid.linestyle'] = '--'

def set_plot_style(ax, title, xlabel=None, ylabel=None):
    if title:
        ax.set_title(title, fontsize=14, pad=20)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=12, labelpad=10)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12, labelpad=10)
    ax.tick_params(labelsize=10)
sns.set_style("whitegrid")  # 设置seaborn样式
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['lines.linewidth'] = 2

def plot_action_distribution(data_dir, output_dir):
    """Plot distribution of actions in dataset"""
    actions = os.listdir(data_dir)
    action_counts = {action: len(os.listdir(os.path.join(data_dir, action))) 
                    for action in actions if os.path.isdir(os.path.join(data_dir, action))}
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x=list(action_counts.keys()), y=list(action_counts.values()))
    set_plot_style(plt.gca(), 
                  title='Action Type Distribution',
                  xlabel='Action Type',
                  ylabel='Sample Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'action_distribution.png'))
    plt.close()
    return list(action_counts.keys())

def plot_sample_visualizations(data_dir, output_dir, data_type='uwb'):
    """Generate sample visualizations for each action"""
    from doppler_visualization import plot_point_cloud, plot_3d_doppler
    
    actions = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    
    for action in actions:
        action_dir = os.path.join(data_dir, action)
        # Filter files based on data type
        if data_type == 'uwb':
            samples = [f for f in sorted(os.listdir(action_dir)) if f.endswith('.jpg')][:3]
        else:
            samples = [f for f in sorted(os.listdir(action_dir)) if f.endswith('.txt')][:3]
        
        for i, sample in enumerate(samples):
            sample_path = os.path.join(action_dir, sample)
            
            # Load and process data based on type
            if data_type == 'uwb':
                # For UWB data, load image directly
                data = np.array(Image.open(sample_path))
                
                # Generate Doppler visualization
                save_path = os.path.join(output_dir, f'{action}_sample{i+1}_doppler.png')
                plot_3d_doppler(None, None, data, action, data_type='uwb', save_path=save_path)
                
                # Convert to point cloud and visualize
                convert_to_point_cloud = get_uwb_adapter()
                points = convert_to_point_cloud(sample_path)
                save_path = os.path.join(output_dir, f'{action}_sample{i+1}_pointcloud.png')
                plot_point_cloud(points, action, data_type='uwb', save_path=save_path)
            else:
                # For mmWave data or text files, load text file
                with open(sample_path, 'r') as f:
                    lines = f.readlines()
                points = []
                for line in lines:
                    if line.strip():
                        try:
                            x, y, z, intensity = map(float, line.strip().split())
                            points.append([x, y, z, intensity])
                        except ValueError:
                            continue
                data = np.array(points)
                
                # Generate point cloud visualization
                save_path = os.path.join(output_dir, f'{action}_sample{i+1}_pointcloud.png')
                plot_point_cloud(data, action, data_type='mmwave', save_path=save_path)
                
                # Generate Doppler visualization
                save_path = os.path.join(output_dir, f'{action}_sample{i+1}_doppler.png')
                f = np.linspace(0, data.shape[0], data.shape[0])
                t = np.linspace(0, data.shape[1], data.shape[1])
                plot_3d_doppler(f, t, data, action, data_type='mmwave', save_path=save_path)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate visualizations for radar data')
    parser.add_argument('--data_dir', required=True, help='Data directory')
    parser.add_argument('--output_dir', required=True, help='Output directory')
    parser.add_argument('--data_type', default='mmwave', choices=['mmwave', 'uwb'],
                      help='Type of radar data')
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Generate visualizations
    actions = plot_action_distribution(args.data_dir, args.output_dir)
    plot_sample_visualizations(args.data_dir, args.output_dir, args.data_type)
    
    print("Generated visualizations:")
    print("1. action_distribution.png - Action type distribution")
    print("2. Point cloud visualizations:")
    for action in actions:
        print(f"   - {action}_sampleX_pointcloud.png")
    print("3. Doppler spectrograms:")
    for action in actions:
        print(f"   - {action}_sampleX_doppler.png")

if __name__ == "__main__":
    main()
