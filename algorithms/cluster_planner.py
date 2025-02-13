import numpy as np
import networkx as nx
from typing import List, Tuple, Dict, Optional
from sklearn.cluster import SpectralClustering
from environment import Environment
from algorithms.neural_ahpp import NeuralAHPP

class ClusterPlanner:
    """Multi-drone cluster-based path planning"""
    
    def __init__(self, env: Environment, num_drones: int):
        self.env = env
        self.num_drones = num_drones
        self.num_clusters = max(1, num_drones // 3)  # Adaptive cluster size
        self.cluster_radius = 50.0  # Dynamic cluster radius
        self.cluster_assignments = None
        self.topology = nx.Graph()
        self.planners = [NeuralAHPP(env) for _ in range(num_drones)]
        
    def adaptive_clustering(self, positions: np.ndarray) -> np.ndarray:
        """Adaptive clustering based on drone positions"""
        # Build similarity matrix
        n = len(positions)
        similarity = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                dist = np.linalg.norm(positions[i] - positions[j])
                similarity[i, j] = np.exp(-dist / self.cluster_radius)
                
        # Perform spectral clustering
        clustering = SpectralClustering(
            n_clusters=self.num_clusters,
            affinity='precomputed',
            random_state=42
        )
        clusters = clustering.fit_predict(similarity)
        return clusters
        
    def update_topology(self) -> None:
        """Update communication topology based on clustering"""
        self.topology.clear()
        
        # Add nodes
        for i in range(self.num_drones):
            self.topology.add_node(i)
            
        # Add edges within clusters
        for i in range(self.num_drones):
            for j in range(i + 1, self.num_drones):
                if self.cluster_assignments[i] == self.cluster_assignments[j]:
                    self.topology.add_edge(i, j)
                    
        # Add edges between cluster leaders
        cluster_leaders = {}
        for i in range(self.num_drones):
            cluster = self.cluster_assignments[i]
            if cluster not in cluster_leaders:
                cluster_leaders[cluster] = i
                
        leader_list = list(cluster_leaders.values())
        for i in range(len(leader_list)):
            for j in range(i + 1, len(leader_list)):
                self.topology.add_edge(leader_list[i], leader_list[j])
                
    def plan_paths(self, starts: List[np.ndarray], goals: List[np.ndarray]) -> List[np.ndarray]:
        """Plan paths for all drones"""
        assert len(starts) == len(goals) == self.num_drones
        
        # Initial clustering
        positions = np.array(starts)
        self.cluster_assignments = self.adaptive_clustering(positions)
        self.update_topology()
        
        # Plan paths for each drone
        paths = []
        for i in range(self.num_drones):
            # Get neighboring drones
            neighbors = list(self.topology.neighbors(i))
            
            # Plan path considering neighbors
            path = self.plan_single_path(i, starts[i], goals[i], 
                                       [starts[j] for j in neighbors],
                                       [goals[j] for j in neighbors])
            paths.append(path)
            
        return paths
        
    def plan_single_path(self, drone_id: int, start: np.ndarray, goal: np.ndarray,
                        neighbor_starts: List[np.ndarray], 
                        neighbor_goals: List[np.ndarray]) -> np.ndarray:
        """Plan path for single drone considering neighbors"""
        planner = self.planners[drone_id]
        
        # Add virtual obstacles for collision avoidance
        original_obstacles = self.env.obstacles.copy()
        for n_start, n_goal in zip(neighbor_starts, neighbor_goals):
            # Add cylindrical obstacle along neighbor's path
            direction = n_goal - n_start
            distance = np.linalg.norm(direction)
            if distance > 0:
                direction = direction / distance
                num_points = max(2, int(distance / 20))
                for t in range(num_points):
                    point = n_start + direction * (t * distance / (num_points - 1))
                    virtual_obstacle = (point[0], point[1], point[2], 
                                     5.0, 5.0, 5.0, 0, 'cylinder')
                    self.env.obstacles.append(virtual_obstacle)
                    
        # Plan path with multiple attempts
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                path = planner.plan_path(start, goal)
                if path is not None:
                    break
            except ValueError:
                if attempt == max_attempts - 1:
                    # If all attempts fail, return straight line path
                    path = np.array([start, goal])
                continue
            
        # Restore original obstacles
        self.env.obstacles = original_obstacles
        return path
        
    def update_clusters(self, current_positions: List[np.ndarray]) -> None:
        """Update clusters based on current positions"""
        positions = np.array(current_positions)
        self.cluster_assignments = self.adaptive_clustering(positions)
        self.update_topology()
        
    def get_cluster_info(self) -> Dict:
        """Get information about current clustering"""
        if self.cluster_assignments is None:
            return {}
            
        info = {
            'num_clusters': self.num_clusters,
            'assignments': self.cluster_assignments.tolist(),
            'topology': list(self.topology.edges())
        }
        return info
