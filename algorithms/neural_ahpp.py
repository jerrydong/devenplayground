import numpy as np
import tensorflow as tf
from environment import Environment
import random
from collections import deque
import math
import time
import logging
from typing import List, Tuple, Dict, Optional
from algorithms.dynamic_predictor import DynamicPredictor
from algorithms.rrt_star import RRTStar

logger = logging.getLogger(__name__)

class NeuralAHPP:
    """Enhanced Neural-Augmented Hybrid Path Planning"""
    
    def __init__(self, env: Environment):
        self.env = env
        self.model = self.create_neural_network()
        self.experience_buffer = deque(maxlen=10000)
        self.min_radius = 20.0
        self.max_radius = 100.0
        self.exploration_factor = 0.2
        self.dynamic_predictor = DynamicPredictor()
        self.obstacle_history = {}
        self.weights = {'safety': 0.4, 'time': 0.3, 'energy': 0.3}
        self.weight_update_rate = 0.1
        
    def train_neural_network(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train neural network with experience replay"""
        obstacle_positions = np.array([[x, y, z] for x, y, z, *_ in self.env.obstacles])
        obstacle_positions = np.tile(obstacle_positions, (len(X), 1, 1))
        self.model.fit([X, obstacle_positions], y, batch_size=32, epochs=1, verbose=0)
        
    def create_neural_network(self) -> tf.keras.Model:
        """Enhanced neural network with attention mechanism"""
        # Input layers
        state_input = tf.keras.Input(shape=(9,))
        obstacle_input = tf.keras.Input(shape=(None, 3))
        
        # Process state information
        x1 = tf.keras.layers.Dense(128)(state_input)
        x1 = tf.keras.layers.BatchNormalization()(x1)
        x1 = tf.keras.layers.Activation('relu')(x1)
        x1 = tf.keras.layers.Dropout(0.3)(x1)
        
        # Process obstacle information with attention
        attention = tf.keras.layers.MultiHeadAttention(
            num_heads=4, key_dim=32
        )(obstacle_input, obstacle_input)
        x2 = tf.keras.layers.GlobalAveragePooling1D()(attention)
        
        # Combine processed information
        combined = tf.keras.layers.Concatenate()([x1, x2])
        x = tf.keras.layers.Dense(64, activation='relu')(combined)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Dropout(0.2)(x)
        
        # Output layer
        outputs = tf.keras.layers.Dense(3)(x)
        
        model = tf.keras.Model(inputs=[state_input, obstacle_input], outputs=outputs)
        
        def path_planning_loss(y_true, y_pred):
            mse_loss = tf.keras.losses.mean_squared_error(y_true, y_pred)
            # Enhanced smoothness loss with curvature penalty
            diff1 = tf.experimental.numpy.diff(y_pred, axis=0)
            diff2 = tf.experimental.numpy.diff(diff1, axis=0)
            smoothness_loss = tf.reduce_mean(tf.square(diff1)) + tf.reduce_mean(tf.square(diff2))
            return mse_loss + 0.3 * smoothness_loss  # Increased smoothness weight
            
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                     loss=path_planning_loss)
        return model
        
    def calculate_reward(self, current: np.ndarray, new_point: np.ndarray, 
                        goal: np.ndarray) -> float:
        """Calculate comprehensive reward"""
        # Distance to goal reward
        goal_dist = np.linalg.norm(new_point - goal)
        goal_reward = -goal_dist / np.linalg.norm(self.env.size)
        
        # Obstacle clearance reward
        min_clearance = float('inf')
        for obs in self.env.obstacles:
            x, y, z, a, b, c, theta, shape = obs
            center = np.array([x, y, z])
            clearance = np.linalg.norm(new_point - center) - max(a, b, c)
            min_clearance = min(min_clearance, clearance)
        clearance_reward = np.clip(min_clearance / 50.0, -1.0, 1.0)
        
        # Enhanced path smoothness reward with curvature consideration
        smoothness = 0.0
        if len(self.experience_buffer) >= 2:
            prev = list(self.experience_buffer)[-2]
            curr = list(self.experience_buffer)[-1]
            v1 = curr - prev
            v2 = new_point - curr
            angle = np.arccos(np.clip(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)), -1.0, 1.0))
            smoothness = -angle / np.pi  # Normalized angle-based smoothness
        
        # Dynamic obstacle prediction reward
        dynamic_reward = 0.0
        for obs_id in self.obstacle_history:
            pred_positions, uncertainties = self.dynamic_predictor.predict_trajectory(obs_id)
            if pred_positions is not None:
                min_future_dist = min(np.linalg.norm(new_point - pos) for pos in pred_positions)
                dynamic_reward -= 1.0 / (1.0 + min_future_dist)
        
        # Combine rewards using adaptive weights
        total_reward = (
            self.weights['safety'] * (clearance_reward + 0.5 * dynamic_reward) +
            self.weights['time'] * goal_reward +
            self.weights['energy'] * smoothness
        )
        return total_reward
        
    def update_weights(self, safety_score: float, time_score: float, 
                      energy_score: float) -> None:
        """Update weights based on performance metrics"""
        total_score = safety_score + time_score + energy_score
        if total_score == 0:
            return
            
        new_weights = {
            'safety': safety_score / total_score,
            'time': time_score / total_score,
            'energy': energy_score / total_score
        }
        
        for key in self.weights:
            self.weights[key] = ((1 - self.weight_update_rate) * self.weights[key] +
                                self.weight_update_rate * new_weights[key])
                                
    def get_adaptive_sample(self, nodes: List[np.ndarray], goal: np.ndarray) -> np.ndarray:
        """Neural-guided adaptive sampling"""
        if len(self.experience_buffer) > 0 and random.random() > self.exploration_factor:
            experience = random.choice(list(self.experience_buffer))
            return experience + np.random.normal(0, 0.1, size=3)
        
        if random.random() < 0.2:
            return np.array(goal)
            
        sample = np.random.rand(3) * self.env.size
        obstacle_positions = np.array([[x, y, z] for x, y, z, *_ in self.env.obstacles])
        
        input_data = [
            np.concatenate([sample, goal, nodes[-1]]).reshape(1, 9),
            obstacle_positions.reshape(1, -1, 3)
        ]
        
        adjustment = self.model.predict(input_data, verbose=0)[0]
        return sample + 0.1 * adjustment
        
    def near_neighbors(self, nodes: List[np.ndarray], node: np.ndarray) -> List[int]:
        """Dynamic radius adjustment based on environment complexity"""
        distances = [np.linalg.norm(n - node) for n in nodes]
        
        # Calculate local obstacle density
        sample_points = np.random.uniform(low=-20, high=20, size=(20, 3)) + node
        obstacle_count = sum(1 for p in sample_points if self.env.is_collision(p))
        obstacle_density = obstacle_count / 20.0
        
        # Adjust radius based on density and node count
        base_radius = 40.0 * (np.log(len(nodes)) / len(nodes)) ** (1 / 3)
        density_factor = 1.0 - obstacle_density
        
        radius = np.clip(base_radius * density_factor, self.min_radius, self.max_radius)
        return [i for i, d in enumerate(distances) if d <= radius]
        
    def neural_optimize(self, path: np.ndarray) -> np.ndarray:
        """Enhanced path optimization with experience replay"""
        optimized_path = [path[0]]
        obstacle_positions = np.array([[x, y, z] for x, y, z, *_ in self.env.obstacles])
        
        for i in range(1, len(path) - 1):
            prev, current, next_point = path[i-1], path[i], path[i+1]
            
            input_data = [
                np.concatenate([prev, current, next_point]).reshape(1, 9),
                obstacle_positions.reshape(1, -1, 3)
            ]
            
            prediction = self.model.predict(input_data, verbose=0)[0]
            new_point = current + 0.1 * prediction
            
            if not self.env.is_collision(new_point):
                reward = self.calculate_reward(current, new_point, path[-1])
                self.experience_buffer.append(new_point)
                optimized_path.append(new_point)
                
                if len(self.experience_buffer) >= 32:
                    batch = random.sample(list(self.experience_buffer), 32)
                    X = np.array([np.concatenate([p-0.1, p, p+0.1]) for p in batch])
                    y = np.array([p for p in batch])
                    self.train_neural_network(X, y)
            else:
                optimized_path.append(current)
                
        optimized_path.append(path[-1])
        return np.array(optimized_path)
        
    def plan_path(self, start: np.ndarray, goal: np.ndarray) -> Optional[np.ndarray]:
        """Enhanced path planning with dynamic obstacle prediction and robust fallback"""
        try:
            # Track dynamic obstacles
            current_time = time.time()
            for i, obs in enumerate(self.env.obstacles):
                pos = np.array(obs[:3])
                self.dynamic_predictor.update_history(i, pos, current_time)
            
            # Initial path planning using RRT* with optimized parameters
            rrt = RRTStar(self.env, max_iter=5000, step_size=2.0, goal_sample_rate=0.2)
            initial_path = rrt.plan(start, goal)
            
            if initial_path is None:
                logger.warning("First RRT* attempt failed, trying with different parameters...")
                # Fallback to RRT* with different parameters
                rrt = RRTStar(self.env, max_iter=8000, step_size=1.0, goal_sample_rate=0.3)
                initial_path = rrt.plan(start, goal)
                
            if initial_path is None:
                logger.warning("Second RRT* attempt failed, trying with more conservative parameters...")
                # Second fallback with more conservative parameters
                rrt = RRTStar(self.env, max_iter=10000, step_size=0.5, goal_sample_rate=0.4)
                initial_path = rrt.plan(start, goal)
                
            if initial_path is not None:
                try:
                    # Neural optimization
                    neural_path = self.neural_optimize(initial_path)
                    
                    if neural_path is not None:
                        # Calculate performance metrics
                        safety_score = self.calculate_safety_score(neural_path)
                        time_score = self.calculate_time_score(neural_path)
                        energy_score = self.calculate_energy_score(neural_path)
                        
                        # Update weights
                        self.update_weights(safety_score, time_score, energy_score)
                        
                        # Check for dynamic replanning need
                        for i in range(len(self.env.obstacles)):
                            pred_positions, uncertainties = self.dynamic_predictor.predict_trajectory(i)
                            if pred_positions is not None and any(u > self.dynamic_predictor.uncertainty_threshold 
                                                            for u in uncertainties):
                                return self.plan_path(start, goal)
                        
                        return self.ensure_start_to_goal(neural_path, start, goal)
                    return initial_path
                except Exception as e:
                    logger.warning(f"Neural optimization failed: {e}")
                    return initial_path  # Fallback to RRT* path if neural optimization fails
            
            return None
            
        except Exception as e:
            logger.warning(f"Path planning failed: {e}")
            return None
        
    def calculate_safety_score(self, path: np.ndarray) -> float:
        min_clearance = float('inf')
        for point in path:
            for obs in self.env.obstacles:
                x, y, z, a, b, c, theta, shape = obs
                center = np.array([x, y, z])
                clearance = np.linalg.norm(point - center) - max(a, b, c)
                min_clearance = min(min_clearance, clearance)
        return np.clip(min_clearance / 50.0, 0.1, 1.0)
        
    def calculate_time_score(self, path: np.ndarray) -> float:
        path_length = sum(np.linalg.norm(path[i+1] - path[i]) 
                         for i in range(len(path)-1))
        direct_length = np.linalg.norm(path[-1] - path[0])
        return np.clip(direct_length / path_length, 0.1, 1.0)
        
    def calculate_energy_score(self, path: np.ndarray) -> float:
        total_angle = 0
        for i in range(1, len(path)-1):
            v1 = path[i] - path[i-1]
            v2 = path[i+1] - path[i]
            angle = np.arccos(np.dot(v1, v2) / 
                            (np.linalg.norm(v1) * np.linalg.norm(v2)))
            total_angle += angle
        return np.clip(1.0 - total_angle / (np.pi * len(path)), 0.1, 1.0)
        
    def ensure_start_to_goal(self, path: np.ndarray, start: np.ndarray, 
                            goal: np.ndarray) -> np.ndarray:
        if not np.array_equal(path[0], start):
            path = np.vstack([start, path])
        if not np.array_equal(path[-1], goal):
            path = np.vstack([path, goal])
        return path
