import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.patches import Circle, PathPatch
import mpl_toolkits.mplot3d.art3d as art3d
from metrics import calculate_path_metrics
from environment import Environment
import seaborn as sns

def plot_3d_path_with_obstacles(path, env, title="3D Path Planning Result"):
    """Create 3D visualization of path with obstacles"""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot path
    path = np.array(path)
    ax.plot(path[:, 0], path[:, 1], path[:, 2], 'b-', linewidth=2, label='Planned Path')
    ax.scatter(path[0, 0], path[0, 1], path[0, 2], c='g', marker='o', s=100, label='Start')
    ax.scatter(path[-1, 0], path[-1, 1], path[-1, 2], c='r', marker='*', s=100, label='Goal')
    
    # Plot obstacles
    for obs in env.obstacles:
        x, y, z, a, b, c, theta, shape = obs
        if shape == 'cube':
            plot_cube(ax, (x, y, z), (a, b, c))
        elif shape == 'cylinder':
            plot_cylinder(ax, (x, y, z), (a, b, c))
        elif shape == 'sphere':
            plot_sphere(ax, (x, y, z), a)
    
    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)
    ax.legend()
    
    # Set equal aspect ratio
    ax.set_box_aspect([1, 1, 1])
    
    return fig

def plot_cluster_formation(paths, env, title="Cluster Formation"):
    """Visualize cluster formation and paths"""
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot paths for each drone
    colors = plt.cm.rainbow(np.linspace(0, 1, len(paths)))
    for i, (path, color) in enumerate(zip(paths, colors)):
        path = np.array(path)
        ax.plot(path[:, 0], path[:, 1], path[:, 2], 
                color=color, linewidth=2, label=f'Drone {i+1}')
        ax.scatter(path[0, 0], path[0, 1], path[0, 2], 
                  color=color, marker='o', s=100)
        ax.scatter(path[-1, 0], path[-1, 1], path[-1, 2], 
                  color=color, marker='*', s=100)
    
    # Plot obstacles
    for obs in env.obstacles:
        x, y, z, a, b, c, theta, shape = obs
        if shape == 'cube':
            plot_cube(ax, (x, y, z), (a, b, c), alpha=0.3)
        elif shape == 'cylinder':
            plot_cylinder(ax, (x, y, z), (a, b, c), alpha=0.3)
        elif shape == 'sphere':
            plot_sphere(ax, (x, y, z), a, alpha=0.3)
    
    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Set equal aspect ratio
    ax.set_box_aspect([1, 1, 1])
    
    return fig

def plot_performance_comparison(metrics_dict, title="Algorithm Performance Comparison"):
    """Create performance comparison visualization"""
    # Prepare data
    algorithms = list(metrics_dict.keys())
    metrics = list(metrics_dict[algorithms[0]].keys())
    
    # Create subplots
    n_metrics = len(metrics)
    n_cols = 3
    n_rows = (n_metrics + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
    axes = axes.flatten()
    
    # Plot each metric
    for i, metric in enumerate(metrics):
        if '_std' not in metric:  # Skip standard deviation entries
            values = [metrics_dict[alg][metric] for alg in algorithms]
            errors = [metrics_dict[alg].get(metric + '_std', 0) for alg in algorithms]
            
            ax = axes[i]
            bars = ax.bar(algorithms, values, yerr=errors, capsize=5)
            
            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}', ha='center', va='bottom')
            
            ax.set_title(metric)
            ax.tick_params(axis='x', rotation=45)
    
    # Remove empty subplots
    for i in range(len(metrics), len(axes)):
        fig.delaxes(axes[i])
    
    plt.suptitle(title)
    plt.tight_layout()
    
    return fig

def plot_cube(ax, center, size, alpha=0.3):
    """Plot a cube on the 3D axis"""
    x, y, z = center
    dx, dy, dz = size
    
    # Create arrays for the vertices and edges
    xx = np.array([[x-dx/2, x+dx/2, x+dx/2, x-dx/2, x-dx/2],
                   [x-dx/2, x+dx/2, x+dx/2, x-dx/2, x-dx/2]])
    yy = np.array([[y-dy/2, y-dy/2, y+dy/2, y+dy/2, y-dy/2],
                   [y-dy/2, y-dy/2, y+dy/2, y+dy/2, y-dy/2]])
    zz = np.array([[z-dz/2, z-dz/2, z-dz/2, z-dz/2, z-dz/2],
                   [z+dz/2, z+dz/2, z+dz/2, z+dz/2, z+dz/2]])
    
    # Plot the six faces
    for i in range(2):
        ax.plot_surface(xx[i:i+1], yy[i:i+1], zz[i:i+1], alpha=alpha, color='gray')
    
    xx = xx.T
    yy = yy.T
    zz = zz.T
    for i in range(2):
        ax.plot_surface(xx[i:i+1], yy[i:i+1], zz[i:i+1], alpha=alpha, color='gray')
    
    xx = xx.T
    yy = yy.T
    zz = zz.T
    for i in range(2):
        ax.plot_surface(xx[i:i+1], yy[i:i+1], zz[i:i+1], alpha=alpha, color='gray')

def plot_cylinder(ax, center, size, alpha=0.3):
    """Plot a cylinder on the 3D axis"""
    x, y, z = center
    radius, _, height = size
    
    # Create cylinder
    theta = np.linspace(0, 2*np.pi, 32)
    z_points = np.array([z - height/2, z + height/2])
    theta_grid, z_grid = np.meshgrid(theta, z_points)
    
    x_grid = x + radius * np.cos(theta_grid)
    y_grid = y + radius * np.sin(theta_grid)
    
    # Plot surface
    ax.plot_surface(x_grid, y_grid, z_grid, alpha=alpha, color='gray')
    
    # Plot top and bottom circles
    for z_val in z_points:
        circle = Circle((x, y), radius, alpha=alpha, color='gray')
        ax.add_patch(circle)
        art3d.pathpatch_2d_to_3d(circle, z=z_val)

def plot_sphere(ax, center, radius, alpha=0.3):
    """Plot a sphere on the 3D axis"""
    x, y, z = center
    
    # Create sphere
    u = np.linspace(0, 2 * np.pi, 32)
    v = np.linspace(0, np.pi, 32)
    x_grid = x + radius * np.outer(np.cos(u), np.sin(v))
    y_grid = y + radius * np.outer(np.sin(u), np.sin(v))
    z_grid = z + radius * np.outer(np.ones(np.size(u)), np.cos(v))
    
    # Plot surface
    ax.plot_surface(x_grid, y_grid, z_grid, alpha=alpha, color='gray')

def create_animation(paths, env, title="Path Planning Animation"):
    """Create animation of multiple paths"""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot obstacles
    for obs in env.obstacles:
        x, y, z, a, b, c, theta, shape = obs
        if shape == 'cube':
            plot_cube(ax, (x, y, z), (a, b, c), alpha=0.2)
        elif shape == 'cylinder':
            plot_cylinder(ax, (x, y, z), (a, b, c), alpha=0.2)
        elif shape == 'sphere':
            plot_sphere(ax, (x, y, z), a, alpha=0.2)
    
    # Set up lines and points for animation
    lines = []
    points = []
    colors = plt.cm.rainbow(np.linspace(0, 1, len(paths)))
    
    for path, color in zip(paths, colors):
        line, = ax.plot([], [], [], color=color, linewidth=2)
        point, = ax.plot([], [], [], color=color, marker='o', markersize=8)
        lines.append(line)
        points.append(point)
    
    # Animation update function
    def update(frame):
        for i, (line, point, path) in enumerate(zip(lines, points, paths)):
            if frame < len(path):
                line.set_data(path[:frame+1, 0], path[:frame+1, 1])
                line.set_3d_properties(path[:frame+1, 2])
                point.set_data([path[frame, 0]], [path[frame, 1]])
                point.set_3d_properties([path[frame, 2]])
        return lines + points
    
    # Set axis limits and labels
    max_coords = np.max([np.max(path, axis=0) for path in paths], axis=0)
    min_coords = np.min([np.min(path, axis=0) for path in paths], axis=0)
    margin = (max_coords - min_coords) * 0.1
    
    ax.set_xlim(min_coords[0] - margin[0], max_coords[0] + margin[0])
    ax.set_ylim(min_coords[1] - margin[1], max_coords[1] + margin[1])
    ax.set_zlim(min_coords[2] - margin[2], max_coords[2] + margin[2])
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)
    
    # Create animation
    max_frames = max(len(path) for path in paths)
    anim = animation.FuncAnimation(fig, update, frames=max_frames,
                                 interval=50, blit=True)
    
    return anim

def save_visualization_results(env, neural_path, dynamic_paths, cluster_paths, 
                             metrics_dict, output_dir="results"):
    """Save all visualization results"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Static path planning result
    fig1 = plot_3d_path_with_obstacles(neural_path, env, 
                                     "Neural Evolution Path Planning")
    fig1.savefig(os.path.join(output_dir, "neural_evolution_path.png"), 
                 dpi=300, bbox_inches='tight')
    plt.close(fig1)
    
    # 2. Dynamic environment paths
    fig2 = plot_3d_path_with_obstacles(dynamic_paths[0], env,
                                     "Dynamic Environment Path Planning")
    fig2.savefig(os.path.join(output_dir, "dynamic_environment_path.png"),
                 dpi=300, bbox_inches='tight')
    plt.close(fig2)
    
    # 3. Cluster formation
    fig3 = plot_cluster_formation(cluster_paths, env,
                                "Multi-Drone Cluster Formation")
    fig3.savefig(os.path.join(output_dir, "cluster_formation.png"),
                 dpi=300, bbox_inches='tight')
    plt.close(fig3)
    
    # 4. Performance comparison
    fig4 = plot_performance_comparison(metrics_dict,
                                     "Algorithm Performance Comparison")
    fig4.savefig(os.path.join(output_dir, "performance_comparison.png"),
                 dpi=300, bbox_inches='tight')
    plt.close(fig4)
    
    # 5. Create and save animation
    anim = create_animation(cluster_paths, env, 
                          "Multi-Drone Path Planning Animation")
    anim.save(os.path.join(output_dir, "path_planning_animation.gif"),
              writer='pillow')
    plt.close()
    
    return {
        "neural_path": os.path.join(output_dir, "neural_evolution_path.png"),
        "dynamic_path": os.path.join(output_dir, "dynamic_environment_path.png"),
        "cluster_formation": os.path.join(output_dir, "cluster_formation.png"),
        "performance_comparison": os.path.join(output_dir, "performance_comparison.png"),
        "animation": os.path.join(output_dir, "path_planning_animation.gif")
    }
