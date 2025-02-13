import numpy as np
from environment import Environment
from algorithms.neural_ahpp import NeuralAHPP
from algorithms.rrt_star import RRTStar
from experiments.visualization_enhanced_v2 import EnhancedVisualizerV2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_path_smoothness():
    """Test and visualize path smoothness improvements"""
    # Create test environment
    env = Environment(size=np.array([100, 100, 100]))
    env.obstacles = [
        (20, 20, 20, 5, 5, 5, 0, 'cube'),
        (50, 50, 50, 8, 8, 8, 0, 'sphere'),
        (80, 80, 80, 6, 6, 10, 0, 'cylinder')
    ]
    
    # Initialize planners
    rrt = RRTStar(env)
    neural = NeuralAHPP(env)
    
    # Test points
    start = np.array([10, 10, 10])
    goal = np.array([90, 90, 90])
    
    # Plan paths
    rrt_path = rrt.plan(start, goal)
    neural_path = neural.plan_path(start, goal)
    
    # Initialize visualizer
    viz = EnhancedVisualizerV2()
    
    # Visualize paths
    paths = {
        'RRT*': rrt_path,
        'Neural-AHPP': neural_path
    }
    
    # Plot comparison
    viz.plot_3d_comparison(paths, env, "Path Planning Smoothness Comparison",
                          chapter=3, category='performance', subcategory='analysis')
    
    # Calculate smoothness metrics
    def calculate_smoothness(path):
        if path is None or len(path) < 3:
            return 0.0
        angles = []
        for i in range(1, len(path)-1):
            v1 = path[i] - path[i-1]
            v2 = path[i+1] - path[i]
            angle = np.arccos(np.clip(np.dot(v1, v2) / 
                            (np.linalg.norm(v1) * np.linalg.norm(v2)), -1.0, 1.0))
            angles.append(angle)
        return 1.0 - np.mean(angles) / np.pi
    
    rrt_smoothness = calculate_smoothness(rrt_path)
    neural_smoothness = calculate_smoothness(neural_path)
    
    logger.info(f"RRT* Smoothness Score: {rrt_smoothness:.3f}")
    logger.info(f"Neural-AHPP Smoothness Score: {neural_smoothness:.3f}")

if __name__ == "__main__":
    test_path_smoothness()
