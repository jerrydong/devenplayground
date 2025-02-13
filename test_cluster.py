import numpy as np
from environment import Environment
from algorithms.cluster_planner import ClusterPlanner

def test_cluster_planner():
    # Create environment with obstacles
    env = Environment(size=np.array([100, 100, 100]))
    env.obstacles = [
        (20, 20, 20, 5, 5, 5, 0, 'cube'),
        (50, 50, 50, 8, 8, 8, 0, 'sphere'),
        (80, 80, 80, 6, 6, 10, 0, 'cylinder')
    ]
    
    # Initialize cluster planner
    planner = ClusterPlanner(env, num_drones=5)
    
    # Define start and goal positions for drones
    starts = [
        np.array([10, 10, 10]),
        np.array([15, 10, 10]),
        np.array([10, 15, 10]),
        np.array([15, 15, 10]),
        np.array([12, 12, 10])
    ]
    
    goals = [
        np.array([90, 90, 90]),
        np.array([85, 90, 90]),
        np.array([90, 85, 90]),
        np.array([85, 85, 90]),
        np.array([88, 88, 90])
    ]
    
    # Plan paths
    paths = planner.plan_paths(starts, goals)
    
    # Verify results
    assert len(paths) == 5, "Should return paths for all drones"
    for path in paths:
        assert len(path) > 0, "Each path should have waypoints"
        assert not any(env.is_collision(p) for p in path), "Paths should be collision-free"
    
    print("Cluster planner test passed successfully!")

if __name__ == "__main__":
    test_cluster_planner()
