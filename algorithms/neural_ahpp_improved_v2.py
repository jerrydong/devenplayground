import numpy as np
import logging
import tensorflow as tf
from typing import Dict, List, Optional
from .neural_ahpp_base import NeuralAHPP

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

class NeuralAHPPImproved(NeuralAHPP):
    """Improved Neural Attention-based Hierarchical Path Planning"""
    
    def __init__(self, env):
        super().__init__(env)
        self.attention_weights = None
        self.experience_buffer = []
        self.buffer_size = 1000
        self.model = None
        self.initialize_model()
        
    def compute_attention(self, state, obstacles):
        """Compute attention weights for obstacles"""
        distances = []
        for obs in obstacles:
            x, y, z = obs[:3]
            dist = np.linalg.norm(state - np.array([x, y, z]))
            distances.append(dist)
        
        # Softmax attention
        attention = np.exp(-np.array(distances))
        self.attention_weights = attention / np.sum(attention)
        return self.attention_weights
        
    def store_experience(self, state, action, reward, next_state):
        """Store experience in replay buffer"""
        if len(self.experience_buffer) >= self.buffer_size:
            self.experience_buffer.pop(0)
        self.experience_buffer.append((state, action, reward, next_state))
        
    def initialize_model(self):
        """Initialize neural network model with improved architecture"""
        try:
            # Configure TensorFlow to use CPU only and set memory growth
            tf.config.set_visible_devices([], 'GPU')
            
            # Enhanced network architecture
            inputs = tf.keras.layers.Input(shape=(9,))  # state(6) + obstacle_features(3)
            
            # Deeper network with residual connections
            x = tf.keras.layers.Dense(128, activation='relu')(inputs)
            x = tf.keras.layers.BatchNormalization()(x)
            x = tf.keras.layers.Dropout(0.2)(x)
            
            # Residual block 1
            skip = x
            x = tf.keras.layers.Dense(128, activation='relu')(x)
            x = tf.keras.layers.BatchNormalization()(x)
            x = tf.keras.layers.Dropout(0.2)(x)
            x = tf.keras.layers.Dense(128, activation=None)(x)  # Match dimensions
            x = tf.keras.layers.Add()([x, skip])
            x = tf.keras.layers.Activation('relu')(x)
            
            # Residual block 2
            skip = x
            x = tf.keras.layers.Dense(128, activation='relu')(x)
            x = tf.keras.layers.BatchNormalization()(x)
            x = tf.keras.layers.Dropout(0.2)(x)
            x = tf.keras.layers.Dense(128, activation=None)(x)  # Match dimensions
            x = tf.keras.layers.Add()([x, skip])
            x = tf.keras.layers.Activation('relu')(x)
            
            # Output layer with normalized actions
            x = tf.keras.layers.Dense(32, activation='relu')(x)
            outputs = tf.keras.layers.Dense(3, activation='tanh')(x)
            
            model = tf.keras.models.Model(inputs=inputs, outputs=outputs)
            
            # Custom learning rate schedule
            lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
                initial_learning_rate=0.001,
                decay_steps=1000,
                decay_rate=0.9
            )
            
            # Compile with custom optimizer and loss
            optimizer = tf.keras.optimizers.Adam(learning_rate=lr_schedule)
            model.compile(optimizer=optimizer, 
                        loss=tf.keras.losses.Huber(),  # More robust to outliers
                        metrics=['mae'])
            
            self.model = model
            
            # Warm up the model with a dummy batch
            dummy_input = tf.zeros((32, 9))
            _ = model.predict(dummy_input, verbose=0)
            
        except Exception as e:
            logger.error(f"Failed to initialize neural network: {e}")
            self.model = None
            
    def predict_action(self, state, batch_size=32):
        """Predict action using neural network with efficient batching"""
        if self.model is None:
            logger.warning("Model not initialized, using heuristic fallback")
            direction = np.random.uniform(-1, 1, 3)
            return direction / np.linalg.norm(direction)
            
        try:
            # Prepare state batch for efficient prediction
            if len(state.shape) == 1:
                state = np.array(state).reshape(1, -1)
            
            # Use model.predict in eval mode
            with tf.device('/CPU:0'):
                action = self.model(state, training=False).numpy()
            
            # Normalize actions
            if len(action.shape) == 2:
                norms = np.linalg.norm(action, axis=1, keepdims=True)
                norms = np.maximum(norms, 1e-8)  # Avoid division by zero
                action = action / norms
            else:
                action = action / np.maximum(np.linalg.norm(action), 1e-8)
            
            return action[0] if len(state.shape) == 2 else action
            
        except Exception as e:
            logger.error(f"Failed to predict action: {e}")
            # Fallback to simple heuristic
            direction = np.random.uniform(-1, 1, 3)
            return direction / np.linalg.norm(direction)
        
    def sample_experience(self, batch_size=32):
        """Sample random batch from experience buffer"""
        if len(self.experience_buffer) < batch_size:
            return None
        indices = np.random.choice(len(self.experience_buffer), batch_size, replace=False)
        return [self.experience_buffer[i] for i in indices]
        
    def plan_path(self, start: np.ndarray, goal: np.ndarray, max_steps: int = 1000) -> Optional[np.ndarray]:
        """Plan path using improved neural network with attention"""
        path = [start]
        current = start.copy()
        step_count = 0
        min_dist_to_goal = float('inf')
        steps_without_improvement = 0
        
        while np.linalg.norm(current - goal) > 0.1 and step_count < max_steps:
            step_count += 1
            
            # Get current state
            state = np.concatenate([current, goal])
            
            # Compute attention weights for obstacles
            attention = self.compute_attention(current, self.env.obstacles)
            
            # Get weighted obstacle features
            obstacle_features = np.zeros(3)
            for w, obs in zip(attention, self.env.obstacles):
                x, y, z = obs[:3]
                obstacle_features += w * np.array([x, y, z])
            
            # Combine state with weighted obstacle features
            augmented_state = np.concatenate([state, obstacle_features])
            
            # Predict action using neural network
            action = self.predict_action(augmented_state)
            
            # Update position
            next_pos = current + action
            
            # Check collision and progress
            if not self.env.is_collision(next_pos):
                current = next_pos
                path.append(current)
                
                # Store experience
                reward = -np.linalg.norm(current - goal)  # Negative distance as reward
                self.store_experience(state, action, reward, np.concatenate([current, goal]))
                
                # Track progress
                dist_to_goal = np.linalg.norm(current - goal)
                if dist_to_goal < min_dist_to_goal:
                    min_dist_to_goal = dist_to_goal
                    steps_without_improvement = 0
                else:
                    steps_without_improvement += 1
                    
                # Break if stuck
                if steps_without_improvement > 50:
                    break
            else:
                # If collision, try random action
                action = np.random.uniform(-1, 1, 3)
                action = action / np.linalg.norm(action)
                next_pos = current + action
                if not self.env.is_collision(next_pos):
                    current = next_pos
                    path.append(current)
                steps_without_improvement += 1
        
        return np.array(path)
