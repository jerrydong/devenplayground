import numpy as np
import tensorflow as tf
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class NeuralAHPP:
    """Base Neural Attention-based Hierarchical Path Planning"""
    
    def __init__(self, env):
        self.env = env
        self.model = None
        self.initialize_model()
        
    def initialize_model(self):
        """Initialize neural network model"""
        try:
            # Configure TensorFlow to use CPU only and reduce retracing
            tf.config.set_visible_devices([], 'GPU')
            tf.config.experimental.enable_tensor_float_32_execution(False)
            
            # Set up TensorFlow function configuration
            tf.config.experimental_run_functions_eagerly(False)
            tf.config.optimizer.set_jit(False)
            
            # Create a function for model prediction to avoid retracing
            @tf.function(reduce_retracing=True, jit_compile=True)
            def predict_fn(inputs):
                return model(inputs, training=False)
            
            # Simple feed-forward network with fixed input shape
            inputs = tf.keras.layers.Input(shape=(6,), batch_size=32)  # state(3) + goal(3)
            x = tf.keras.layers.Dense(64, activation='relu')(inputs)
            x = tf.keras.layers.Dense(32, activation='relu')(x)
            outputs = tf.keras.layers.Dense(3, activation='tanh')(x)  # 3D action space
            
            model = tf.keras.models.Model(inputs=inputs, outputs=outputs)
            model.compile(optimizer='adam', 
                         loss=tf.keras.losses.MeanSquaredError(),
                         metrics=['mae'],
                         run_eagerly=False,
                         jit_compile=True)
            
            self.model = model
            self.predict_fn = predict_fn
            
            # Warm up the model with a dummy batch
            dummy_input = tf.zeros((32, 6))
            _ = self.predict_fn(dummy_input)
            
        except Exception as e:
            logger.error(f"Failed to initialize neural network: {e}")
            self.model = None
            
    def predict_action(self, state):
        """Predict action using neural network"""
        if self.model is None:
            # Fallback to simple heuristic if model initialization failed
            direction = np.random.uniform(-1, 1, 3)
            return direction / np.linalg.norm(direction)
            
        try:
            # Reshape state for model input
            state = tf.convert_to_tensor(state.reshape(1, -1), dtype=tf.float32)
            action = self.predict_fn(state)[0].numpy()
            return action / np.maximum(np.linalg.norm(action), 1e-8)
        except Exception as e:
            logger.error(f"Failed to predict action: {e}")
            # Fallback to simple heuristic
            direction = np.random.uniform(-1, 1, 3)
            return direction / np.linalg.norm(direction)
            
    def plan_path(self, start: np.ndarray, goal: np.ndarray, max_steps: int = 1000) -> Optional[np.ndarray]:
        """Plan path using neural network"""
        path = [start]
        current = start.copy()
        step_count = 0
        min_dist_to_goal = float('inf')
        steps_without_improvement = 0
        
        while np.linalg.norm(current - goal) > 0.1 and step_count < max_steps:
            step_count += 1
            
            # Get current state
            state = np.concatenate([current, goal])
            
            # Predict action using neural network
            action = self.predict_action(state)
            
            # Update position
            next_pos = current + action
            
            # Check collision and progress
            if not self.env.is_collision(next_pos):
                current = next_pos
                path.append(current)
                
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
