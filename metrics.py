import numpy as np
from environment import Environment
from typing import Dict, List, Optional
import time

def calculate_path_smoothness(path: np.ndarray) -> float:
    """Calculate path smoothness using curvature"""
    if len(path) < 3:
        return 1.0
    
    total_curvature = 0
    for i in range(1, len(path)-1):
        v1 = path[i] - path[i-1]
        v2 = path[i+1] - path[i]
        if np.linalg.norm(v1) * np.linalg.norm(v2) > 1e-6:
            cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
            cos_angle = np.clip(cos_angle, -1.0, 1.0)
            angle = np.arccos(cos_angle)
            total_curvature += angle
    
    smoothness = 1.0 - total_curvature / (np.pi * len(path))
    return np.clip(smoothness, 0.0, 1.0)

def calculate_obstacle_clearance(path: np.ndarray, env: Environment) -> float:
    """Calculate minimum clearance from obstacles"""
    min_clearance = float('inf')
    for point in path:
        for obs in env.obstacles:
            x, y, z, a, b, c, theta, shape = obs
            center = np.array([x, y, z])
            clearance = np.linalg.norm(point - center) - max(a, b, c)
            min_clearance = min(min_clearance, clearance)
    return min_clearance

def calculate_dynamic_avoidance_rate(path: np.ndarray, env: Environment, 
                                   time_step: float = 0.1) -> float:
    """Calculate success rate of avoiding dynamic obstacles"""
    total_checks = 0
    successful_avoidance = 0
    
    for i in range(len(path)-1):
        current = path[i]
        next_point = path[i+1]
        time = i * time_step
        
        # Check intermediate points
        for t in np.linspace(0, 1, 5):
            point = current + t * (next_point - current)
            total_checks += 1
            if not env.is_collision(point):
                successful_avoidance += 1
                
    return successful_avoidance / total_checks if total_checks > 0 else 1.0

def calculate_energy_efficiency(path: np.ndarray) -> float:
    """Calculate energy efficiency based on acceleration changes"""
    if len(path) < 3:
        return 1.0
        
    velocities = np.diff(path, axis=0)
    accelerations = np.diff(velocities, axis=0)
    total_acceleration = np.sum(np.linalg.norm(accelerations, axis=1))
    
    # Normalize by path length
    efficiency = 1.0 / (1.0 + total_acceleration / len(path))
    return efficiency

def calculate_path_metrics(path: np.ndarray, env: Environment, 
                         computation_time: Optional[float] = None) -> Dict:
    """Calculate comprehensive path metrics"""
    # Basic metrics
    length = sum(np.linalg.norm(path[i+1] - path[i]) for i in range(len(path)-1))
    collisions = sum(env.is_collision(point) for point in path)
    flight_time = len(path) * 0.1
    
    # Advanced metrics
    smoothness = calculate_path_smoothness(path)
    clearance = calculate_obstacle_clearance(path, env)
    avoidance_rate = calculate_dynamic_avoidance_rate(path, env)
    energy_efficiency = calculate_energy_efficiency(path)
    
    # Efficiency metrics
    direct_distance = np.linalg.norm(path[-1] - path[0])
    path_efficiency = direct_distance / length if length > 0 else 0
    
    metrics = {
        '路径长度': length,
        '碰撞次数': collisions,
        '飞行时间': flight_time,
        '路径平滑度': smoothness,
        '最小障碍物间隙': clearance,
        '避障成功率': avoidance_rate,
        '能量效率': energy_efficiency,
        '路径效率': path_efficiency
    }
    
    if computation_time is not None:
        metrics['计算时间'] = computation_time
        
    return metrics

def evaluate_algorithm(algorithm, env: Environment, start: np.ndarray, 
                      goal: np.ndarray, num_runs: int = 10) -> Dict:
    """Evaluate algorithm performance over multiple runs"""
    all_metrics = []
    computation_times = []
    
    for _ in range(num_runs):
        start_time = time.time()
        path = algorithm.plan_path(start, goal)
        computation_time = time.time() - start_time
        
        metrics = calculate_path_metrics(path, env, computation_time)
        all_metrics.append(metrics)
        computation_times.append(computation_time)
    
    # Calculate average metrics
    avg_metrics = {}
    std_metrics = {}
    
    for key in all_metrics[0].keys():
        values = [m[key] for m in all_metrics]
        avg_metrics[key] = np.mean(values)
        std_metrics[key + '_std'] = np.std(values)
    
    return {**avg_metrics, **std_metrics}

def compare_algorithms(algorithms: Dict, env: Environment, start: np.ndarray, 
                      goal: np.ndarray, num_runs: int = 10) -> Dict:
    """Compare multiple algorithms"""
    results = {}
    for name, alg in algorithms.items():
        results[name] = evaluate_algorithm(alg, env, start, goal, num_runs)
    return results
