import numpy as np
from environment import Environment
from algorithms.cluster_planner import ClusterPlanner
from algorithms.neural_ahpp import NeuralAHPP
import matplotlib.pyplot as plt
import time
from typing import List, Dict, Tuple

def create_test_scenarios():
    """Create test scenarios for cluster evaluation"""
    scenarios = []
    
    # Scenario 1: Search and Rescue
    env1 = Environment(size=np.array([200, 200, 100]))
    env1.obstacles = [
        (50, 50, 30, 20, 20, 40, 0, 'cuboid'),  # Building
        (100, 100, 20, 30, 30, 30, 0, 'cube'),  # Another building
        (150, 150, 25, 15, 15, 35, 0, 'cylinder')  # Tower
    ]
    starts1 = [np.array([10, 10, 50]) + np.random.randn(3) * 5 for _ in range(5)]
    goals1 = [np.array([180, 180, 50]) + np.random.randn(3) * 5 for _ in range(5)]
    scenarios.append((env1, starts1, goals1, "Search and Rescue"))
    
    # Scenario 2: Area Surveillance
    env2 = Environment(size=np.array([300, 300, 80]))
    env2.obstacles = [
        (100, 100, 30, 40, 40, 20, 0, 'cuboid'),  # Large structure
        (200, 200, 25, 25, 25, 30, 0, 'cylinder'),  # Tower
        (150, 150, 20, 30, 30, 15, 0, 'cube')  # Building
    ]
    starts2 = [np.array([20, 20, 40]) + np.random.randn(3) * 5 for _ in range(5)]
    goals2 = [np.array([250, 250, 40]) + np.random.randn(3) * 5 for _ in range(5)]
    scenarios.append((env2, starts2, goals2, "Area Surveillance"))
    
    return scenarios

def evaluate_cluster_performance(planner: ClusterPlanner, 
                               env: Environment,
                               starts: List[np.ndarray],
                               goals: List[np.ndarray]) -> Dict:
    """Evaluate cluster planner performance"""
    start_time = time.time()
    paths = planner.plan_paths(starts, goals)
    computation_time = time.time() - start_time
    
    # Calculate metrics
    path_lengths = [sum(np.linalg.norm(path[i+1] - path[i]) 
                   for i in range(len(path)-1)) for path in paths]
    
    # Formation cohesion
    avg_separation = []
    for i in range(len(paths[0])):
        positions = [path[min(i, len(path)-1)] for path in paths]
        separations = []
        for j in range(len(positions)):
            for k in range(j+1, len(positions)):
                separations.append(np.linalg.norm(positions[j] - positions[k]))
        avg_separation.append(np.mean(separations))
    
    # Collision checks
    collisions = sum(1 for path in paths 
                    for point in path if env.is_collision(point))
    
    return {
        "平均路径长度": np.mean(path_lengths),
        "最大路径长度": max(path_lengths),
        "平均队形间距": np.mean(avg_separation),
        "碰撞次数": collisions,
        "计算时间": computation_time
    }

def plot_cluster_results(env: Environment, 
                        paths: List[np.ndarray],
                        starts: List[np.ndarray],
                        goals: List[np.ndarray],
                        title: str):
    """Plot cluster planning results"""
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot paths
    colors = plt.cm.rainbow(np.linspace(0, 1, len(paths)))
    for path, color in zip(paths, colors):
        ax.plot(path[:, 0], path[:, 1], path[:, 2], 
                color=color, linewidth=2, alpha=0.7)
    
    # Plot starts and goals
    for start in starts:
        ax.scatter(*start, color='g', s=100, label='Start')
    for goal in goals:
        ax.scatter(*goal, color='r', s=100, label='Goal')
    
    # Plot obstacles
    for obs in env.obstacles:
        x, y, z, a, b, c, theta, shape = obs
        if shape == 'cube' or shape == 'cuboid':
            ax.bar3d(x-a/2, y-b/2, z-c/2, a, b, c, color='gray', alpha=0.3)
        elif shape == 'cylinder':
            theta = np.linspace(0, 2*np.pi, 30)
            z_vals = np.linspace(z-c/2, z+c/2, 30)
            theta, z_vals = np.meshgrid(theta, z_vals)
            x_vals = x + a * np.cos(theta)
            y_vals = y + b * np.sin(theta)
            ax.plot_surface(x_vals, y_vals, z_vals, color='gray', alpha=0.3)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)
    plt.savefig(f'cluster_results_{title.lower().replace(" ", "_")}.png')
    plt.close()

def run_comparative_analysis():
    """Run comparative analysis of cluster planning"""
    scenarios = create_test_scenarios()
    results = {}
    
    for env, starts, goals, scenario_name in scenarios:
        # Test cluster planner
        cluster_planner = ClusterPlanner(env, num_drones=len(starts))
        cluster_metrics = evaluate_cluster_performance(cluster_planner, env, starts, goals)
        results[f"Cluster_{scenario_name}"] = cluster_metrics
        
        # Generate and plot results
        paths = cluster_planner.plan_paths(starts, goals)
        plot_cluster_results(env, paths, starts, goals, 
                           f"Cluster Planning - {scenario_name}")
    
    # Print comparative results
    print("\n=== 集群路径规划性能分析 ===")
    for scenario, metrics in results.items():
        print(f"\n{scenario}:")
        for metric, value in metrics.items():
            print(f"{metric}: {value:.3f}")
    
    return results

if __name__ == "__main__":
    run_comparative_analysis()
