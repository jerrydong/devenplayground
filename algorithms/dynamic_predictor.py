import numpy as np
import tensorflow as tf
from typing import Tuple, List, Optional

class DynamicPredictor:
    """LSTM-based dynamic obstacle trajectory prediction"""
    
    def __init__(self, sequence_length: int = 10):
        self.sequence_length = sequence_length
        self.model = self.create_lstm_model()
        self.uncertainty_threshold = 0.2
        self.history_buffer = {}
        
    def create_lstm_model(self) -> tf.keras.Model:
        """Create LSTM model for trajectory prediction"""
        model = tf.keras.Sequential([
            tf.keras.layers.LSTM(64, input_shape=(self.sequence_length, 3), 
                               return_sequences=True),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.LSTM(32),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(6)  # [position (3), uncertainty (3)]
        ])
        
        def custom_loss(y_true, y_pred):
            # Position prediction loss
            mse_loss = tf.keras.losses.mean_squared_error(y_true[:, :3], y_pred[:, :3])
            # Uncertainty estimation loss
            uncertainty_loss = tf.reduce_mean(
                tf.square(y_pred[:, 3:] - tf.abs(y_true[:, :3] - y_pred[:, :3]))
            )
            return mse_loss + 0.2 * uncertainty_loss
            
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                     loss=custom_loss)
        return model
        
    def update_history(self, obstacle_id: int, position: np.ndarray, 
                      timestamp: float) -> None:
        """Update obstacle position history"""
        if obstacle_id not in self.history_buffer:
            self.history_buffer[obstacle_id] = []
        self.history_buffer[obstacle_id].append((timestamp, position))
        
        # Keep only recent history
        while len(self.history_buffer[obstacle_id]) > self.sequence_length:
            self.history_buffer[obstacle_id].pop(0)
            
    def prepare_sequence(self, history: List[Tuple[float, np.ndarray]]) -> np.ndarray:
        """Prepare sequence for LSTM input"""
        positions = [pos for _, pos in history]
        if len(positions) < self.sequence_length:
            # Pad with repeated first position
            padding = [positions[0]] * (self.sequence_length - len(positions))
            positions = padding + positions
        return np.array(positions[-self.sequence_length:])
        
    def predict_trajectory(self, obstacle_id: int, horizon: int = 10) -> Tuple[
            List[np.ndarray], List[float]]:
        """Predict future trajectory with uncertainty"""
        if obstacle_id not in self.history_buffer:
            return None, None
            
        history = self.history_buffer[obstacle_id]
        if len(history) < 2:
            return None, None
            
        sequence = self.prepare_sequence(history)
        sequence = sequence.reshape(1, self.sequence_length, 3)
        
        # Predict multiple steps ahead
        predictions = []
        uncertainties = []
        current_sequence = sequence.copy()
        
        for _ in range(horizon):
            pred = self.model.predict(current_sequence, verbose=0)[0]
            position = pred[:3]
            uncertainty = pred[3:]
            
            predictions.append(position)
            uncertainties.append(np.mean(uncertainty))
            
            # Update sequence for next prediction
            current_sequence = np.roll(current_sequence, -1, axis=1)
            current_sequence[0, -1] = position
            
        return predictions, uncertainties
        
    def update_model(self, obstacle_id: int, actual_position: np.ndarray) -> None:
        """Update prediction model with actual observations"""
        if obstacle_id not in self.history_buffer:
            return
            
        history = self.history_buffer[obstacle_id]
        if len(history) < self.sequence_length + 1:
            return
            
        sequence = self.prepare_sequence(history[:-1])
        target = np.concatenate([actual_position, np.zeros(3)])  # Zero uncertainty for actual
        
        self.model.train_on_batch(
            sequence.reshape(1, self.sequence_length, 3),
            target.reshape(1, 6)
        )
