import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import seaborn as sns
from typing import List, Dict, Any
import os
import logging
import pandas as pd
from matplotlib.patches import Circle, PathPatch
import mpl_toolkits.mplot3d.art3d as art3d
import matplotlib as mpl
import matplotlib.pyplot as plt

# Configure logging
logger = logging.getLogger(__name__)

# Configure matplotlib
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['figure.dpi'] = 300
mpl.rcParams['figure.figsize'] = [12, 8]
mpl.rcParams['figure.autolayout'] = True
mpl.rcParams['font.family'] = 'DejaVu Sans'
mpl.rcParams['axes.unicode_minus'] = False

# ASCII labels for now to avoid font issues
LABELS = {
    'neural_evolution': 'Neural Evolution',
    'dynamic_environment': 'Dynamic Environment',
    'cluster_planning': 'Cluster Planning',
    'path_length': 'Path Length',
    'collision_count': 'Collision Count',
    'flight_time': 'Flight Time',
    'turning_points': 'Turning Points',
    'baseline': 'Baseline',
    'with_experience': 'With Experience',
    'with_attention': 'With Attention',
    'full_model': 'Full Model',
    'simple_scenario': 'Simple Scenario',
    'complex_scenario': 'Complex Scenario',
    'narrow_scenario': 'Narrow Scenario',
    'planned_path': 'Planned Path',
    'start_point': 'Start',
    'end_point': 'Goal',
    'x_axis': 'X',
    'y_axis': 'Y',
    'z_axis': 'Z',
    'metrics': 'Metrics',
    'values': 'Values',
    'metrics_comparison': 'Metrics Comparison',
    'ablation_study': 'Ablation Study',
    'scenario_comparison': 'Scenario Comparison',
    'animation': 'Animation',
    'heatmap': 'Heatmap'
}

class EnhancedVisualizer:
    """Enhanced visualization tools for path planning experiments"""
    
    def __init__(self, output_dir="organized_results"):
        self.output_dir = output_dir
        self.temp_dir = os.path.join(output_dir, "temp")
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        
        # Clean up temp directory
        for f in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, f))
            
        # Define visualization categories
        self.categories = {
            'performance': ['metrics', 'comparison', 'analysis'],
            'ablation': ['components', 'experiments', 'results'],
            'scenarios': ['simple', 'complex', 'dynamic'],
            'animations': ['paths', 'sequences', 'interactive']
        }
        
    def plot_3d_path_with_obstacles(self, path: np.ndarray, env: Any, title: str,
                                     chapter: int = 3, category: str = 'scenarios',
                                     subcategory: str = 'simple') -> str:
        """Plot single path in 3D with obstacles"""
        try:
            fig = plt.figure(figsize=(12, 8))
            ax = fig.add_subplot(111, projection='3d')
            
            # Plot path
            ax.plot(path[:, 0], path[:, 1], path[:, 2], 
                   color='blue', linewidth=2, label=LABELS.get('planned_path', 'Planned Path'))
            ax.scatter(path[0, 0], path[0, 1], path[0, 2], 
                      color='green', marker='o', s=100, label=LABELS.get('start_point', 'Start'))
            ax.scatter(path[-1, 0], path[-1, 1], path[-1, 2], 
                      color='red', marker='*', s=100, label=LABELS.get('end_point', 'Goal'))
            
            # Plot obstacles
            self._plot_obstacles(ax, env)
            
            ax.set_xlabel(LABELS.get('x_axis', 'X'))
            ax.set_ylabel(LABELS.get('y_axis', 'Y'))
            ax.set_zlabel(LABELS.get('z_axis', 'Z'))
            ax.set_title(LABELS.get(title, title))
            ax.legend()
            
            # Save figure
            filename = f"ch{chapter}_{category}_{subcategory}_{title.replace(' ', '_')}.png"
            filepath = os.path.join(self.temp_dir, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            # Move to organized directory
            target_dir = os.path.join(self.output_dir, f"chapter{chapter}", category, subcategory)
            os.makedirs(target_dir, exist_ok=True)
            target_path = os.path.join(target_dir, filename)
            shutil.move(filepath, target_path)
            
            logger.info(f"Generated 3D path visualization: {target_path}")
            return target_path
            
        except Exception as e:
            logger.error(f"Failed to create 3D path visualization: {e}")
            return ""
        
    def plot_3d_comparison(self, paths_dict: Dict[str, np.ndarray], 
                          env: Any, title: str,
                          chapter: int = 3, category: str = 'performance',
                          subcategory: str = 'comparison') -> str:
        """Plot 3D path comparison"""
        try:
            fig = plt.figure(figsize=(15, 10))
            ax = fig.add_subplot(111, projection='3d')
            
            # Plot paths
            colors = plt.cm.rainbow(np.linspace(0, 1, len(paths_dict)))
            for (name, path), color in zip(paths_dict.items(), colors):
                ax.plot(path[:, 0], path[:, 1], path[:, 2], 
                       color=color, linewidth=2, label=LABELS.get(name, name))
                ax.scatter(path[0, 0], path[0, 1], path[0, 2], 
                          color=color, marker='o', s=100)
                ax.scatter(path[-1, 0], path[-1, 1], path[-1, 2], 
                          color=color, marker='*', s=100)
            
            # Plot obstacles
            self._plot_obstacles(ax, env)
            
            ax.set_xlabel(LABELS.get('x_axis', 'X'))
            ax.set_ylabel(LABELS.get('y_axis', 'Y'))
            ax.set_zlabel(LABELS.get('z_axis', 'Z'))
            ax.set_title(LABELS.get(title, title))
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            
            # Save figure
            filename = f"{title.replace(' ', '_')}.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Generated 3D comparison visualization: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to create 3D comparison plot: {e}")
            return ""
        
    def plot_metrics_comparison(self, metrics_dict: Dict[str, Dict[str, float]], 
                              title: str,
                              chapter: int = 3, category: str = 'performance',
                              subcategory: str = 'metrics') -> str:
        """Plot performance metrics comparison"""
        try:
            metrics = list(next(iter(metrics_dict.values())).keys())
            algorithms = list(metrics_dict.keys())
            
            fig, axes = plt.subplots(3, 2, figsize=(15, 20))
            axes = axes.ravel()
            
            for i, metric in enumerate(metrics):
                if i >= len(axes):
                    break
                    
                values = [metrics_dict[alg][metric] for alg in algorithms]
                ax = axes[i]
                bars = ax.bar([LABELS.get(alg, alg) for alg in algorithms], values)
                
                # Add value labels
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.3f}', ha='center', va='bottom')
                
                ax.set_title(LABELS.get(metric, metric))
                ax.tick_params(axis='x', rotation=45)
            
            plt.suptitle(LABELS.get(title, title))
            plt.tight_layout()
            
            filename = f"{title.replace(' ', '_')}.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Generated metrics comparison visualization: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to create metrics comparison plot: {e}")
            return ""
        
    def plot_ablation_study(self, ablation_results: Dict[str, Dict[str, float]], 
                           title: str,
                           chapter: int = 3, category: str = 'ablation',
                           subcategory: str = 'components') -> str:
        """Plot ablation study results"""
        try:
            components = list(ablation_results.keys())
            metrics = list(ablation_results[components[0]].keys())
            
            fig, axes = plt.subplots(len(metrics), 1, figsize=(12, 4*len(metrics)))
            if len(metrics) == 1:
                axes = [axes]
            
            for i, metric in enumerate(metrics):
                values = [ablation_results[comp][metric] for comp in components]
                ax = axes[i]
                bars = ax.bar([LABELS.get(comp, comp) for comp in components], values)
                
                # Add value labels
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.3f}', ha='center', va='bottom')
                
                ax.set_title(f'{LABELS.get(metric, metric)} Ablation Results')
                ax.tick_params(axis='x', rotation=45)
            
            plt.suptitle(LABELS.get(title, title))
            plt.tight_layout()
            
            filename = f"{title.replace(' ', '_')}_ablation.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Generated ablation study visualization: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to create ablation study plot: {e}")
            return ""
        
    def plot_scenario_comparison(self, scenario_results: Dict[str, Dict[str, Dict[str, float]]], 
                               title: str,
                               chapter: int = 3, category: str = 'scenarios',
                               subcategory: str = 'comparison') -> str:
        """Plot algorithm performance comparison across different scenarios"""
        try:
            scenarios = list(scenario_results.keys())
            algorithms = list(next(iter(scenario_results.values())).keys())
            metrics = list(next(iter(next(iter(scenario_results.values())).values())).keys())
            
            fig, axes = plt.subplots(len(metrics), 1, figsize=(15, 5*len(metrics)))
            if len(metrics) == 1:
                axes = [axes]
            
            for i, metric in enumerate(metrics):
                ax = axes[i]
                x = np.arange(len(scenarios))
                width = 0.8 / len(algorithms)
                
                for j, alg in enumerate(algorithms):
                    values = [scenario_results[scene][alg][metric] for scene in scenarios]
                    bars = ax.bar(x + j*width, values, width, 
                                label=LABELS.get(alg, alg))
                    
                    # Add value labels
                    for bar in bars:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height,
                               f'{height:.3f}', ha='center', va='bottom')
                
                ax.set_title(f'{LABELS.get(metric, metric)} Performance Across Scenarios')
                ax.set_xticks(x + width * (len(algorithms)-1)/2)
                ax.set_xticklabels([LABELS.get(s, s) for s in scenarios], rotation=45)
                ax.legend()
            
            plt.suptitle(LABELS.get(title, title))
            plt.tight_layout()
            
            filename = f"{title.replace(' ', '_')}_scenarios.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Generated scenario comparison visualization: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to create scenario comparison plot: {e}")
            return ""
        
    def create_animation(self, paths_dict: Dict[str, np.ndarray], 
                        env: Any, title: str) -> str:
        """Create path planning animation with error handling"""
        try:
            # Instead of animation, create a sequence of static frames
            filename = f"{title.replace(' ', '_')}_path_sequence.png"
            filepath = os.path.join(self.output_dir, filename)
            
            # Create subplot grid for key frames
            num_frames = 4  # Show 4 key frames
            fig = plt.figure(figsize=(20, 5))
            
            for frame_idx in range(num_frames):
                ax = fig.add_subplot(1, num_frames, frame_idx + 1, projection='3d')
                
                # Plot obstacles
                self._plot_obstacles(ax, env)
                
                # Plot paths up to current frame
                colors = plt.cm.rainbow(np.linspace(0, 1, len(paths_dict)))
                for (name, path), color in zip(paths_dict.items(), colors):
                    progress = int((frame_idx + 1) * len(path) / num_frames)
                    ax.plot(path[:progress, 0], path[:progress, 1], path[:progress, 2],
                           color=color, linewidth=2, label=LABELS.get(name, name))
                    if progress > 0:
                        ax.scatter([path[progress-1, 0]], [path[progress-1, 1]], 
                                 [path[progress-1, 2]], color=color, marker='o')
                
                ax.set_xlabel(LABELS.get('x_axis', 'X'))
                ax.set_ylabel(LABELS.get('y_axis', 'Y'))
                ax.set_zlabel(LABELS.get('z_axis', 'Z'))
                ax.set_title(f'Progress: {(frame_idx + 1) * 100 // num_frames}%')
                if frame_idx == 0:
                    ax.legend()
            
            plt.suptitle(LABELS.get(title, title))
            plt.tight_layout()
            
            # Save the sequence plot
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Generated path sequence visualization: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to create path sequence visualization: {e}")
            return ""
        
    def plot_heatmap(self, scenario_results: Dict[str, Dict[str, float]], title: str,
                    chapter: int = 3, category: str = 'performance',
                    subcategory: str = 'analysis') -> str:
        """Plot 3D path density heatmap"""
        try:
            fig = plt.figure(figsize=(15, 10))
            ax = fig.add_subplot(111, projection='3d')
            
            # Create 3D grid for density calculation
            x = np.linspace(0, 200, 20)
            y = np.linspace(0, 200, 20)
            z = np.linspace(0, 100, 10)
            X, Y, Z = np.meshgrid(x, y, z)
            
            # Calculate density
            density = np.zeros_like(X)
            total_paths = 0
            
            for scenario_paths in scenario_results.values():
                if isinstance(scenario_paths, dict):
                    for path in scenario_paths.values():
                        if isinstance(path, np.ndarray) and len(path) > 0:
                            total_paths += 1
                            for point in path:
                                # Find nearest grid points
                                ix = np.searchsorted(x, point[0]) - 1
                                iy = np.searchsorted(y, point[1]) - 1
                                iz = np.searchsorted(z, point[2]) - 1
                                if 0 <= ix < X.shape[0]-1 and 0 <= iy < Y.shape[1]-1 and 0 <= iz < Z.shape[2]-1:
                                    density[ix, iy, iz] += 1
            
            if total_paths > 0:
                density = density / total_paths  # Normalize
                
                # Plot density using scatter with color representing density
                scatter = ax.scatter(X, Y, Z, c=density.flatten(),
                                   cmap='viridis', alpha=0.6)
                plt.colorbar(scatter, label='Path Density')
                
                ax.set_xlabel(LABELS.get('x_axis', 'X'))
                ax.set_ylabel(LABELS.get('y_axis', 'Y'))
                ax.set_zlabel(LABELS.get('z_axis', 'Z'))
                ax.set_title(LABELS.get(title, title))
                
                filename = f"{title.replace(' ', '_')}_heatmap.png"
                filepath = os.path.join(self.output_dir, filename)
                plt.savefig(filepath, dpi=300, bbox_inches='tight')
                plt.close()
                
                logger.info(f"Generated heatmap visualization: {filepath}")
                return filepath
            else:
                logger.warning("No valid paths found for heatmap generation")
                return ""
                
        except Exception as e:
            logger.error(f"Failed to create heatmap: {e}")
            return ""
        
    def _plot_obstacles(self, ax, env):
        """Plot obstacles"""
        for obs in env.obstacles:
            x, y, z, a, b, c, theta, shape = obs
            if shape == 'cube':
                self._plot_cube(ax, (x, y, z), (a, b, c))
            elif shape == 'cylinder':
                self._plot_cylinder(ax, (x, y, z), (a, b, c))
            elif shape == 'sphere':
                self._plot_sphere(ax, (x, y, z), a)
                
    def _plot_cube(self, ax, center, size):
        """Plot cube obstacle"""
        x, y, z = center
        dx, dy, dz = size
        
        xx = np.array([[x-dx/2, x+dx/2, x+dx/2, x-dx/2, x-dx/2],
                       [x-dx/2, x+dx/2, x+dx/2, x-dx/2, x-dx/2]])
        yy = np.array([[y-dy/2, y-dy/2, y+dy/2, y+dy/2, y-dy/2],
                       [y-dy/2, y-dy/2, y+dy/2, y+dy/2, y-dy/2]])
        zz = np.array([[z-dz/2, z-dz/2, z-dz/2, z-dz/2, z-dz/2],
                       [z+dz/2, z+dz/2, z+dz/2, z+dz/2, z+dz/2]])
        
        for i in range(2):
            ax.plot_surface(xx[i:i+1], yy[i:i+1], zz[i:i+1], alpha=0.3, color='gray')
        
        xx = xx.T
        yy = yy.T
        zz = zz.T
        for i in range(2):
            ax.plot_surface(xx[i:i+1], yy[i:i+1], zz[i:i+1], alpha=0.3, color='gray')
        
        xx = xx.T
        yy = yy.T
        zz = zz.T
        for i in range(2):
            ax.plot_surface(xx[i:i+1], yy[i:i+1], zz[i:i+1], alpha=0.3, color='gray')
            
    def _plot_cylinder(self, ax, center, size):
        """Plot cylinder obstacle"""
        x, y, z = center
        radius, _, height = size
        
        theta = np.linspace(0, 2*np.pi, 32)
        z_points = np.array([z - height/2, z + height/2])
        theta_grid, z_grid = np.meshgrid(theta, z_points)
        
        x_grid = x + radius * np.cos(theta_grid)
        y_grid = y + radius * np.sin(theta_grid)
        
        ax.plot_surface(x_grid, y_grid, z_grid, alpha=0.3, color='gray')
        
    def _plot_sphere(self, ax, center, radius):
        """Plot sphere obstacle"""
        x, y, z = center
        
        u = np.linspace(0, 2 * np.pi, 32)
        v = np.linspace(0, np.pi, 32)
        x_grid = x + radius * np.outer(np.cos(u), np.sin(v))
        y_grid = y + radius * np.outer(np.sin(u), np.sin(v))
        z_grid = z + radius * np.outer(np.ones(np.size(u)), np.cos(v))
        
        ax.plot_surface(x_grid, y_grid, z_grid, alpha=0.3, color='gray')
