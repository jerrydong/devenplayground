import numpy as np
import logging
from typing import List, Tuple, Optional

logger = logging.getLogger(__name__)

class RRTStar:
    """RRT* path planning algorithm"""
    
    def __init__(self, env, max_iter=5000, step_size=1.0, goal_sample_rate=0.3):
        self.env = env
        self.max_iter = max_iter
        self.step_size = step_size  # Reduced for finer granularity
        self.goal_sample_rate = goal_sample_rate  # Increased for better goal-directed behavior
        self.min_radius = 5.0  # Reduced for finer connections
        self.max_radius = 30.0  # Reduced for better local optimization
        
    def plan(self, start: np.ndarray, goal: np.ndarray) -> Optional[np.ndarray]:
        """Plan a path from start to goal"""
        try:
            self.start = start
            self.goal = goal
            self.nodes = [start]
            self.parents = {0: None}
            self.costs = {0: 0.0}
            
            for i in range(self.max_iter):
                # Sample random point
                if np.random.random() < self.goal_sample_rate:
                    point = goal
                else:
                    point = np.random.rand(3) * self.env.size
                    
                # Find nearest node
                nearest_idx = self._find_nearest(point)
                nearest_node = self.nodes[nearest_idx]
                
                # Steer towards point
                new_node = self._steer(nearest_node, point)
                if new_node is None:
                    continue
                    
                # Check if path is collision free
                if self._is_collision_free(nearest_node, new_node):
                    # Find nearby nodes
                    try:
                        nearby_indices = self._find_nearby(new_node)
                    except Exception as e:
                        logger.warning(f"Error finding nearby nodes: {e}")
                        continue
                    
                    # Find best parent
                    min_cost = self.costs[nearest_idx] + np.linalg.norm(new_node - nearest_node)
                    best_parent_idx = nearest_idx
                    
                    for idx in nearby_indices:
                        try:
                            cost = self.costs[idx] + np.linalg.norm(new_node - self.nodes[idx])
                            if cost < min_cost and self._is_collision_free(self.nodes[idx], new_node):
                                min_cost = cost
                                best_parent_idx = idx
                        except Exception as e:
                            logger.warning(f"Error computing cost for node {idx}: {e}")
                            continue
                    
                    # Add node
                    new_idx = len(self.nodes)
                    self.nodes.append(new_node)
                    self.parents[new_idx] = best_parent_idx
                    self.costs[new_idx] = min_cost
                    
                    # Rewire nearby nodes
                    for idx in nearby_indices:
                        try:
                            cost = min_cost + np.linalg.norm(new_node - self.nodes[idx])
                            if cost < self.costs[idx] and self._is_collision_free(new_node, self.nodes[idx]):
                                self.parents[idx] = new_idx
                                self.costs[idx] = cost
                        except Exception as e:
                            logger.warning(f"Error rewiring node {idx}: {e}")
                            continue
                    
                    # Check if goal is reached
                    if np.linalg.norm(new_node - goal) < self.step_size:
                        path = self._extract_path(new_idx)
                        if path is not None:
                            return self._smooth_path(path)
            
            # If no path found, try to connect to closest node to goal
            closest_idx = self._find_nearest(goal)
            if np.linalg.norm(self.nodes[closest_idx] - goal) < self.step_size * 2:
                path = self._extract_path(closest_idx)
                if path is not None:
                    return self._smooth_path(path)
                    
        except Exception as e:
            logger.error(f"Error in RRT* planning: {e}")
            return None
                
        return None
        
    def _find_nearest(self, point: np.ndarray) -> int:
        """Find nearest node index"""
        distances = [np.linalg.norm(node - point) for node in self.nodes]
        return np.argmin(distances)
        
    def _find_nearby(self, point: np.ndarray) -> List[int]:
        """Find nearby nodes within dynamic radius"""
        try:
            n = len(self.nodes)
            radius = min(self.max_radius, 
                        max(self.min_radius, 
                            self.step_size * (np.log(max(2, n)) / max(1, n)) ** (1/3)))
            
            nearby = []
            point = np.array(point, dtype=np.float64)
            for i, node in enumerate(self.nodes):
                try:
                    node = np.array(node, dtype=np.float64)
                    if np.sum((node - point) ** 2) ** 0.5 <= radius:
                        nearby.append(i)
                except Exception as e:
                    logger.warning(f"Error computing distance for node {i}: {e}")
                    continue
                    
            return nearby
            
        except Exception as e:
            logger.warning(f"Error finding nearby nodes: {e}")
            return []
        
    def _steer(self, from_node: np.ndarray, to_node: np.ndarray) -> Optional[np.ndarray]:
        """Steer from one node towards another"""
        direction = to_node - from_node
        distance = np.linalg.norm(direction)
        
        if distance < 1e-6:
            return None
            
        if distance > self.step_size:
            direction = direction / distance * self.step_size
            
        new_node = from_node + direction
        
        # Check if new node is within bounds with margin
        margin = 5.0
        if not all(margin <= x <= s - margin for x, s in zip(new_node, self.env.size)):
            return None
            
        # Check if path to new node is collision-free
        if self.env.is_collision(new_node):
            return None
            
        return new_node
        
    def _is_collision_free(self, from_node: np.ndarray, to_node: np.ndarray) -> bool:
        """Check if path between nodes is collision free"""
        direction = to_node - from_node
        distance = np.linalg.norm(direction)
        
        if distance < 1e-6:
            return True
            
        # Check intermediate points
        num_points = max(2, int(distance / (self.step_size / 2)))
        for i in range(num_points):
            point = from_node + direction * i / (num_points - 1)
            if self.env.is_collision(point):
                return False
                
        return True
        
    def _extract_path(self, end_idx: int) -> Optional[np.ndarray]:
        """Extract path from start to end node"""
        path = []
        current_idx = end_idx
        
        while current_idx is not None:
            path.append(self.nodes[current_idx])
            current_idx = self.parents[current_idx]
            
        if len(path) < 2:
            return None
            
        return np.array(list(reversed(path)))
        
    def _smooth_path(self, path: np.ndarray) -> np.ndarray:
        """Enhanced path smoothing using interpolation and shortcutting"""
        if len(path) < 3:
            return path
            
        # Initial shortcutting
        smoothed = [path[0]]
        current_idx = 0
        while current_idx < len(path) - 1:
            for i in range(len(path) - 1, current_idx, -1):
                if self._is_collision_free(path[current_idx], path[i]):
                    smoothed.append(path[i])
                    current_idx = i
                    break
            else:
                current_idx += 1
                smoothed.append(path[current_idx])
        
        smoothed = np.array(smoothed)
        
        # Additional smoothing using interpolation
        final_path = [smoothed[0]]
        for i in range(len(smoothed)-1):
            start = smoothed[i]
            end = smoothed[i+1]
            dist = np.linalg.norm(end - start)
            
            # Add intermediate points for long segments
            if dist > self.step_size * 2:
                num_points = int(dist / self.step_size)
                for j in range(1, num_points):
                    alpha = j / num_points
                    point = start + alpha * (end - start)
                    if not self.env.is_collision(point):
                        final_path.append(point)
            
            final_path.append(end)
            
        return np.array(final_path)
