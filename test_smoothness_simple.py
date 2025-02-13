import numpy as np
from environment import Environment
from algorithms.rrt_star import RRTStar
from experiments.visualization_enhanced_v2 import EnhancedVisualizerV2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_rrt_smoothness():
    """Test RRT* path smoothness improvements"""
    # Create simple test environment
    env = Environment(size=np.array([100, 100, 100]))
    env.obstacles = [
        (50, 50, 50, 10, 10, 10, 0, 'sphere')  # Single obstacle for simplicity
    ]
    
    # Initialize planner
    rrt = RRTStar(env, max_iter=2000, step_size=1.0, goal_sample_rate=0.3)
    
    # Test points
    start = np.array([10, 10, 10])
    goal = np.array([90, 90, 90])
    
    # Plan path
    path = rrt.plan(start, goal)
    
    if path is None:
        logger.error("Failed to find path")
        return
    
    # Initialize visualizer
    viz = EnhancedVisualizerV2()
    
    # Visualize path
    viz.plot_3d_path_with_obstacles(path, env, "RRT* Path Smoothness Test",
                                  chapter=3, category='performance', subcategory='analysis')
    
    # Calculate smoothness metrics
    def calculate_smoothness(path):
        if len(path) < 3:
            return 0.0
        angles = []
        for i in range(1, len(path)-1):
            v1 = path[i] - path[i-1]
            v2 = path[i+1] - path[i]
            angle = np.arccos(np.clip(np.dot(v1, v2) / 
                            (np.linalg.norm(v1) * np.linalg.norm(v2)), -1.0, 1.0))
            angles.append(angle)
        return 1.0 - np.mean(angles) / np.pi
    
    smoothness = calculate_smoothness(path)
    logger.info(f"Path length: {sum(np.linalg.norm(path[i+1] - path[i]) for i in range(len(path)-1)):.3f}")
    logger.info(f"Number of waypoints: {len(path)}")
    logger.info(f"Smoothness Score: {smoothness:.3f}")

if __name__ == "__main__":
    test_rrt_smoothness()
