from dataclasses import dataclass, field
from typing import List, Dict, Any
import numpy as np

@dataclass
class ExperimentConfig:
    """实验配置"""
    # 基础环境参数
    env_size: List[int] = field(default_factory=lambda: [200, 200, 100])
    num_obstacles: int = 10
    obstacle_types: List[str] = field(default_factory=lambda: ['cube', 'cylinder', 'sphere'])
    
    # 神经进化算法参数
    population_size: int = 100
    mutation_rate: float = 0.1
    crossover_rate: float = 0.8
    num_generations: int = 50
    
    # 动态环境参数
    prediction_horizon: int = 10
    update_frequency: float = 0.1
    uncertainty_threshold: float = 0.2
    
    # 集群规划参数
    num_drones: int = 5
    communication_range: float = 50.0
    formation_radius: float = 20.0
    
    # 实验场景
    scenarios: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        'simple': {
            'num_obstacles': 5,
            'obstacle_size': (10, 10, 10),
            'description': '简单场景-少量静态障碍物'
        },
        'complex': {
            'num_obstacles': 15,
            'obstacle_size': (15, 15, 20),
            'description': '复杂场景-密集静态障碍物'
        },
        'dynamic': {
            'num_obstacles': 8,
            'obstacle_size': (12, 12, 15),
            'moving_obstacles': True,
            'description': '动态场景-移动障碍物'
        },
        'narrow': {
            'num_obstacles': 12,
            'obstacle_size': (30, 5, 20),
            'description': '狭窄场景-窄通道'
        },
        'urban': {
            'num_obstacles': 20,
            'obstacle_size': (20, 20, 40),
            'description': '城市场景-高层建筑'
        }
    })
    
    def __post_init__(self):
        if self.obstacle_types is None:
            self.obstacle_types = ['cube', 'cylinder', 'sphere']
            
        if self.scenarios is None:
            self.scenarios = {
                'simple': {
                    'num_obstacles': 5,
                    'obstacle_size': (10, 10, 10),
                    'description': '简单场景-少量静态障碍物'
                },
                'complex': {
                    'num_obstacles': 15,
                    'obstacle_size': (15, 15, 20),
                    'description': '复杂场景-密集静态障碍物'
                },
                'dynamic': {
                    'num_obstacles': 8,
                    'obstacle_size': (12, 12, 15),
                    'moving_obstacles': True,
                    'description': '动态场景-移动障碍物'
                },
                'narrow': {
                    'num_obstacles': 12,
                    'obstacle_size': (30, 5, 20),
                    'description': '狭窄场景-窄通道'
                },
                'urban': {
                    'num_obstacles': 20,
                    'obstacle_size': (20, 20, 40),
                    'description': '城市场景-高层建筑'
                }
            }

@dataclass
class AblationConfig:
    """消融实验配置"""
    # 神经进化算法消融实验
    neural_evolution_ablation = {
        'baseline': {
            'use_experience_replay': False,
            'use_attention': False,
            'adaptive_sampling': False
        },
        'with_experience_replay': {
            'use_experience_replay': True,
            'use_attention': False,
            'adaptive_sampling': False
        },
        'with_attention': {
            'use_experience_replay': True,
            'use_attention': True,
            'adaptive_sampling': False
        },
        'full_model': {
            'use_experience_replay': True,
            'use_attention': True,
            'adaptive_sampling': True
        }
    }
    
    # 动态预测消融实验
    dynamic_prediction_ablation = {
        'baseline': {
            'use_lstm': False,
            'use_uncertainty': False,
            'use_attention': False
        },
        'with_lstm': {
            'use_lstm': True,
            'use_uncertainty': False,
            'use_attention': False
        },
        'with_uncertainty': {
            'use_lstm': True,
            'use_uncertainty': True,
            'use_attention': False
        },
        'full_model': {
            'use_lstm': True,
            'use_uncertainty': True,
            'use_attention': True
        }
    }
    
    # 集群规划消融实验
    cluster_planning_ablation = {
        'baseline': {
            'use_adaptive_clustering': False,
            'use_attention': False,
            'use_formation': False
        },
        'with_adaptive_clustering': {
            'use_adaptive_clustering': True,
            'use_attention': False,
            'use_formation': False
        },
        'with_attention': {
            'use_adaptive_clustering': True,
            'use_attention': True,
            'use_formation': False
        },
        'full_model': {
            'use_adaptive_clustering': True,
            'use_attention': True,
            'use_formation': True
        }
    }

@dataclass
class ComparisonConfig:
    """算法对比实验配置"""
    baseline_algorithms = {
        'RRT*': {
            'algorithm': 'RRTStar',
            'params': {'max_iter': 1000, 'step_size': 5.0}
        },
        'A*': {
            'algorithm': 'AStar',
            'params': {'heuristic': 'euclidean'}
        },
        'PRM': {
            'algorithm': 'PRM',
            'params': {'num_samples': 1000, 'k': 5}
        }
    }
    
    dynamic_algorithms = {
        'DWA': {
            'algorithm': 'DynamicWindowApproach',
            'params': {'window_size': 5, 'prediction_time': 3.0}
        },
        'APF': {
            'algorithm': 'ArtificialPotentialField',
            'params': {'repulsive_gain': 100, 'attractive_gain': 1.0}
        },
        'MPC': {
            'algorithm': 'ModelPredictiveControl',
            'params': {'horizon': 10, 'dt': 0.1}
        }
    }
    
    cluster_algorithms = {
        'DMPC': {
            'algorithm': 'DistributedMPC',
            'params': {'horizon': 5, 'num_drones': 5}
        },
        'CBS': {
            'algorithm': 'ConflictBasedSearch',
            'params': {'max_iterations': 1000}
        },
        'PSO': {
            'algorithm': 'ParticleSwarmOptimization',
            'params': {'num_particles': 50, 'iterations': 100}
        }
    }

def create_experiment_suite():
    """创建完整实验套件"""
    experiment_config = ExperimentConfig()
    ablation_config = AblationConfig()
    comparison_config = ComparisonConfig()
    
    return {
        'experiment': experiment_config,
        'ablation': ablation_config,
        'comparison': comparison_config
    }
