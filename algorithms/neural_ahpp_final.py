import numpy as np
from .neural_ahpp_improved import NeuralAHPPImproved

class NeuralAHPPFinal(NeuralAHPPImproved):
    """Final version of Neural Attention-based Hierarchical Path Planning with all improvements"""
    
    def __init__(self, env):
        super().__init__(env)
        self.adaptive_lr = 0.001
        self.min_lr = 0.0001
        self.max_lr = 0.01
        self.success_history = []
        self.history_size = 50
        
    def adjust_learning_rate(self, success):
        """Adjust learning rate based on recent performance"""
        self.success_history.append(success)
        if len(self.success_history) > self.history_size:
            self.success_history.pop(0)
            
        # Calculate success rate
        success_rate = sum(self.success_history) / len(self.success_history)
        
        # Adjust learning rate
        if success_rate > 0.9:
            self.adaptive_lr *= 0.95  # Reduce learning rate when performing well
        elif success_rate < 0.7:
            self.adaptive_lr *= 1.05  # Increase learning rate when struggling
            
        # Clip learning rate
        self.adaptive_lr = np.clip(self.adaptive_lr, self.min_lr, self.max_lr)
        
    def predict_action(self, state):
        """Enhanced action prediction with uncertainty estimation"""
        # Add noise for exploration
        noise = np.random.normal(0, 0.1, 3)
        
        # Get base prediction
        action = super().predict_action(state)
        
        # Add adaptive noise based on learning rate
        exploration = noise * (self.adaptive_lr / self.max_lr)
        
        # Combine and normalize
        action = action + exploration
        action = action / np.linalg.norm(action)
        
        return action
        
    def plan_path(self, start, goal):
        """Plan path using final version with all improvements"""
        path = [start]
        current = start.copy()
        success = False
        
        while np.linalg.norm(current - goal) > 0.1:
            # Get current state
            state = np.concatenate([current, goal])
            
            # Compute attention weights for obstacles
            attention = self.compute_attention(current, self.env.obstacles)
            
            # Get weighted obstacle features
            obstacle_features = np.zeros(3)
            for w, obs in zip(attention, self.env.obstacles):
                x, y, z = obs[:3]
                obstacle_features += w * np.array([x, y, z])
            
            # Get experience from buffer
            experience = self.sample_experience(batch_size=1)
            if experience:
                exp_state, exp_action, exp_reward, _ = experience[0]
                # Use experience to guide action if similar state
                if np.linalg.norm(exp_state - state) < 5.0:
                    action = exp_action
                else:
                    # Predict action using neural network with uncertainty
                    action = self.predict_action(np.concatenate([state, obstacle_features]))
            else:
                # Predict action using neural network with uncertainty
                action = self.predict_action(np.concatenate([state, obstacle_features]))
            
            # Update position
            next_pos = current + action
            
            # Check collision
            if not self.env.is_collision(next_pos):
                current = next_pos
                path.append(current)
                
                # Store experience
                reward = -np.linalg.norm(current - goal)  # Negative distance as reward
                self.store_experience(state, action, reward, np.concatenate([current, goal]))
                
                if np.linalg.norm(current - goal) < 1.0:
                    success = True
            else:
                # If collision, try random action
                action = np.random.uniform(-1, 1, 3)
                action = action / np.linalg.norm(action)
                next_pos = current + action
                if not self.env.is_collision(next_pos):
                    current = next_pos
                    path.append(current)
                    
                success = False
            
            # Adjust learning rate based on success
            self.adjust_learning_rate(success)
        
        return np.array(path)
