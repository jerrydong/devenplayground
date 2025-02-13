import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, Circle
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import Axes3D, art3d
import logging
from scipy.ndimage import label
from environment import Environment
import plotly.graph_objects as go
from config import SCENARIOS, OBSTACLE_COLOR

logger = logging.getLogger(__name__)

def plot_3d_obstacles(ax, obstacles, color=OBSTACLE_COLOR, alpha=0.5):
    """Helper function to plot 3D obstacles"""
    for x, y, z, a, b, c, theta, shape in obstacles:
        if shape in ['cube', 'cuboid']:
            # Create vertices for cuboid
            vertices = []
            for dx, dy, dz in itertools.product([-1, 1], repeat=3):
                vertex = np.array([x + dx*a/2, y + dy*b/2, z + dz*c/2])
                vertices.append(vertex)
            # Create 3D polygon collection
            faces = art3d.Poly3DCollection([vertices], alpha=alpha, color=color)
            ax.add_collection3d(faces)
        elif shape == 'cylinder':
            # Create cylinder
            theta_vals = np.linspace(0, 2*np.pi, 30)
            z_vals = np.linspace(z-c/2, z+c/2, 30)
            theta_vals, z_vals = np.meshgrid(theta_vals, z_vals)
            x_vals = x + a * np.cos(theta_vals)
            y_vals = y + b * np.sin(theta_vals)
            surf = ax.plot_surface(x_vals, y_vals, z_vals, color=color, alpha=alpha)
        elif shape == 'ellipsoid':
            # Create ellipsoid
            u = np.linspace(0, 2*np.pi, 20)
            v = np.linspace(0, np.pi, 20)
            x_vals = x + a * np.outer(np.cos(u), np.sin(v))
            y_vals = y + b * np.outer(np.sin(u), np.sin(v))
            z_vals = z + c * np.outer(np.ones_like(u), np.cos(v))
            surf = ax.plot_surface(x_vals, y_vals, z_vals, color=color, alpha=alpha)

def plot_results(env: Environment, paths, algorithms, start, goal, plot_number):
    """Plot path planning results in 3D and 2D"""
    fig = plt.figure(figsize=(20, 10))
    
    # 3D plot
    ax1 = fig.add_subplot(121, projection='3d')
    colors = ['#FF4136', '#2ECC40', '#0074D9']
    
    # Plot paths
    for path, alg, color in zip(paths, algorithms, colors):
        if len(path) < 2:
            logger.warning(f"{alg} 的路径无效，跳过绘图")
            continue
        ax1.plot(path[:, 0], path[:, 1], path[:, 2], color=color, linewidth=2, label=alg)
    
    # Plot start-goal line
    ax1.plot([start[0], goal[0]], [start[1], goal[1]], [start[2], goal[2]], 
             'gray', linestyle='--', linewidth=2)
    
    # Plot obstacles
    plot_3d_obstacles(ax1, env.obstacles)
    
    # Plot start and goal points
    ax1.scatter(*start, color='#FFDC00', s=200, label='起点', edgecolors='black', linewidth=1.5)
    ax1.scatter(*goal, color='#B10DC9', s=200, label='终点', edgecolors='black', linewidth=1.5)
    
    # Set labels and title
    ax1.set_xlabel('X', fontweight='bold')
    ax1.set_ylabel('Y', fontweight='bold')
    ax1.set_zlabel('Z', fontweight='bold')
    ax1.set_title(f'3D 路径规划对比 (场景{plot_number})', fontsize=16, fontweight='bold')
    
    # 2D plot (top view)
    ax2 = fig.add_subplot(122)
    for path, alg, color in zip(paths, algorithms, colors):
        if len(path) < 2:
            continue
        ax2.plot(path[:, 0], path[:, 1], color=color, linewidth=2, label=alg)
    
    # Plot 2D obstacles
    for x, y, z, a, b, c, theta, shape in env.obstacles:
        if shape in ['cube', 'cuboid']:
            rect = Rectangle((x-a/2, y-b/2), a, b, color=OBSTACLE_COLOR, alpha=0.5)
            ax2.add_artist(rect)
        else:
            circle = Circle((x, y), max(a, b), color=OBSTACLE_COLOR, alpha=0.5)
            ax2.add_artist(circle)
    
    # Plot start and goal points
    ax2.scatter(start[0], start[1], color='#FFDC00', s=200, label='起点', 
                edgecolors='black', linewidth=1.5)
    ax2.scatter(goal[0], goal[1], color='#B10DC9', s=200, label='终点', 
                edgecolors='black', linewidth=1.5)
    
    # Create legend
    legend_elements = [Line2D([0], [0], color=color, label=alg) 
                      for color, alg in zip(colors, algorithms)]
    legend_elements.extend([
        Line2D([0], [0], marker='o', color='#FFDC00', label='起点', 
               markerfacecolor='#FFDC00', markersize=10),
        Line2D([0], [0], marker='o', color='#B10DC9', label='终点', 
               markerfacecolor='#B10DC9', markersize=10)
    ])
    ax2.legend(handles=legend_elements, loc='upper left')
    
    ax2.set_xlabel('X', fontweight='bold')
    ax2.set_ylabel('Y', fontweight='bold')
    ax2.set_title(f'2D 路径规划对比 (场景{plot_number}) (俯视图)', 
                  fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'path_planning_results_{plot_number}.png', dpi=300, bbox_inches='tight')
    logger.info(f"结果图 {plot_number} 已保存为 'path_planning_results_{plot_number}.png'")
    plt.close()

def get_scenario_start_goal(scenario_index):
    """Get start and goal positions for a scenario"""
    return SCENARIOS[scenario_index - 1] if 0 < scenario_index <= len(SCENARIOS) else (None, None)

def plot_composite_results(env: Environment, paths_with_scenarios, algorithm_names, algorithm_color_map):
    """Plot composite results for multiple scenarios"""
    fig = plt.figure(figsize=(20, 10))
    ax1 = fig.add_subplot(121, projection='3d')
    
    unique_algorithm_names = list(set(algorithm_names))
    color_map = {name: algorithm_color_map[name] for name in unique_algorithm_names}
    
    # Set axis limits
    ax1.set_xlim([0, env.size[0]])
    ax1.set_ylim([0, env.size[1]])
    ax1.set_zlim([0, env.size[2]])
    
    # Plot paths and points
    for scenario, path in paths_with_scenarios:
        if len(path) < 2:
            logger.warning(f"场景 {scenario} 的路径无效，跳过绘图")
            continue
        
        alg_name = algorithm_names[(scenario - 1) % len(algorithm_names)]
        color = color_map.get(alg_name, 'black')
        ax1.plot(path[:, 0], path[:, 1], path[:, 2], color=color, linewidth=2)
        
        start, goal = get_scenario_start_goal(scenario)
        if start is not None and goal is not None:
            ax1.scatter(*start, color='#FFDC00', s=100, edgecolors='black')
            ax1.scatter(*goal, color='#B10DC9', s=100, edgecolors='black')
    
    # Plot obstacles
    plot_3d_obstacles(ax1, env.obstacles)
    
    # Create legend
    legend_elements = [Line2D([0], [0], color=color_map[name], label=name) 
                      for name in unique_algorithm_names]
    ax1.legend(handles=legend_elements, loc='upper left')
    
    # Set labels and title
    ax1.set_xlabel('X', fontweight='bold')
    ax1.set_ylabel('Y', fontweight='bold')
    ax1.set_zlabel('Z', fontweight='bold')
    ax1.set_title('综合 3D 路径规划对比', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('composite_path_planning_results.png', dpi=300, bbox_inches='tight')
    logger.info("综合结果图已保存为 'composite_path_planning_results.png'")
    plt.close()














