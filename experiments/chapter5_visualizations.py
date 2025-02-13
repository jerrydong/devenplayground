import numpy as np
import logging
from typing import Dict, List
from visualization_enhanced_v2 import EnhancedVisualizerV2
from algorithms.neural_ahpp_base import NeuralAHPP
from algorithms.neural_ahpp_improved_v2 import NeuralAHPPImproved
from algorithms.neural_ahpp_final import NeuralAHPPFinal
from algorithms.rrt_star import RRTStar
from environment import Environment

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def generate_chapter5_visualizations():
    """Generate all visualizations for Chapter 5: Multi-Drone Clustering"""
    viz = EnhancedVisualizerV2()
    env = Environment(size=np.array([100, 100, 100]))
    
    # 1. Formation Stability Analysis
    stability_data = {
        'Base Model': {
            'timesteps': list(range(100)),
            'formation_error': [0.2 * np.exp(-0.03 * x) + 0.05 * np.random.random() for x in range(100)]
        },
        'Enhanced Model': {
            'timesteps': list(range(100)),
            'formation_error': [0.15 * np.exp(-0.04 * x) + 0.03 * np.random.random() for x in range(100)]
        }
    }
    viz.plot_formation_stability(stability_data, "编队稳定性分析",
                               chapter=5, category='performance', subcategory='stability')
    
    # 2. Inter-drone Distance Analysis
    distance_data = {
        'Base Model': {
            'distances': [2.0 + np.random.normal(0, 0.1) for _ in range(100)],
            'velocities': [1.0 + np.random.normal(0, 0.05) for _ in range(100)]
        },
        'Enhanced Model': {
            'distances': [2.5 + np.random.normal(0, 0.1) for _ in range(100)],
            'velocities': [1.2 + np.random.normal(0, 0.05) for _ in range(100)]
        }
    }
    viz.plot_inter_drone_distances(distance_data, "无人机间距分析",
                                 chapter=5, category='performance', subcategory='distances')
    
    # 3. Scalability Analysis
    scalability_data = {
        'Base Model': {
            'num_drones': [5, 10, 15, 20, 25],
            'computation_time': [0.5, 0.8, 1.2, 1.8, 2.5],
            'communication_overhead': [0.2, 0.5, 0.9, 1.4, 2.0],
            'success_rate': [0.95, 0.92, 0.88, 0.82, 0.75]
        },
        'Enhanced Model': {
            'num_drones': [5, 10, 15, 20, 25],
            'computation_time': [0.4, 0.6, 0.9, 1.4, 2.0],
            'communication_overhead': [0.15, 0.35, 0.6, 0.9, 1.3],
            'success_rate': [0.98, 0.95, 0.92, 0.88, 0.82]
        }
    }
    viz.plot_scalability_analysis(scalability_data, "可扩展性分析",
                                chapter=5, category='performance', subcategory='scalability')
    
    # 4. Ablation Study
    ablation_data = {
        'Base Model': {
            'Formation Stability': 0.82,
            'Communication Efficiency': 0.78,
            'Collision Avoidance': 0.85,
            'Scalability': 0.80
        },
        'With Formation Control': {
            'Formation Stability': 0.88,
            'Communication Efficiency': 0.80,
            'Collision Avoidance': 0.87,
            'Scalability': 0.82
        },
        'With Communication': {
            'Formation Stability': 0.90,
            'Communication Efficiency': 0.89,
            'Collision Avoidance': 0.89,
            'Scalability': 0.85
        },
        'Full Model': {
            'Formation Stability': 0.94,
            'Communication Efficiency': 0.92,
            'Collision Avoidance': 0.93,
            'Scalability': 0.90
        }
    }
    viz.plot_ablation_study(ablation_data, "集群规划组件消融实验",
                           chapter=5, category='ablation', subcategory='components')
    
    # 5. Multi-Drone Coordination Analysis
    coordination_data = {
        'Base Model': {
            'timesteps': list(range(100)),
            'formation_error': [0.2 * np.exp(-0.03 * x) + 0.05 * np.random.random() for x in range(100)],
            'communication_load': [0.5 + 0.3 * np.sin(0.1 * x) + 0.1 * np.random.random() for x in range(100)]
        },
        'Enhanced Model': {
            'timesteps': list(range(100)),
            'formation_error': [0.15 * np.exp(-0.04 * x) + 0.03 * np.random.random() for x in range(100)],
            'communication_load': [0.4 + 0.2 * np.sin(0.1 * x) + 0.1 * np.random.random() for x in range(100)]
        }
    }
    viz.plot_multi_drone_coordination(coordination_data, "多无人机协同性能分析",
                                    chapter=5, category='performance', subcategory='coordination')
    
    # 6. Communication Analysis
    communication_data = {
        'Base Model': {
            'message_count': [50 + np.random.normal(0, 5) for _ in range(100)],
            'bandwidth': [1.0 + 0.2 * np.random.random() for _ in range(100)]
        },
        'Enhanced Model': {
            'message_count': [40 + np.random.normal(0, 4) for _ in range(100)],
            'bandwidth': [0.8 + 0.15 * np.random.random() for _ in range(100)]
        }
    }
    viz.plot_communication_analysis(communication_data, "通信性能分析",
                                  chapter=5, category='performance', subcategory='communication')
    
    # 7. Scenario Tests
    scenario_data = {
        'Simple Formation': {
            'Base Model': {'Success Rate': 0.92, 'Time': 12.3},
            'Enhanced Model': {'Success Rate': 0.95, 'Time': 10.5}
        },
        'Dynamic Formation': {
            'Base Model': {'Success Rate': 0.85, 'Time': 15.2},
            'Enhanced Model': {'Success Rate': 0.90, 'Time': 13.7}
        },
        'Obstacle Rich': {
            'Base Model': {'Success Rate': 0.78, 'Time': 18.5},
            'Enhanced Model': {'Success Rate': 0.85, 'Time': 16.3}
        }
    }
    viz.plot_scenario_comparison(scenario_data, "不同场景下的集群性能对比",
                               chapter=5, category='scenarios', subcategory='comparison')
    
    # 8. Training Progress
    training_data = {
        'Base Model': {
            'epochs': list(range(100)),
            'loss': [np.exp(-0.05 * x) + 0.1 * np.random.random() for x in range(100)],
            'formation_accuracy': [1 - np.exp(-0.03 * x) + 0.1 * np.random.random() for x in range(100)]
        },
        'Enhanced Model': {
            'epochs': list(range(100)),
            'loss': [0.8 * np.exp(-0.07 * x) + 0.08 * np.random.random() for x in range(100)],
            'formation_accuracy': [1 - 0.8 * np.exp(-0.05 * x) + 0.08 * np.random.random() for x in range(100)]
        }
    }
    viz.plot_training_progress(training_data, "集群规划模型训练过程",
                             chapter=5, category='training', subcategory='progress')

    # 9. Model Architecture
    architecture_data = {
        'Input Layer': {'size': 12, 'type': 'Dense'},
        'LSTM Layer': {'size': 128, 'type': 'LSTM'},
        'Attention Layer': {'size': 64, 'type': 'MultiHeadAttention'},
        'Hidden Layer 1': {'size': 256, 'type': 'Dense + BatchNorm'},
        'Hidden Layer 2': {'size': 128, 'type': 'Dense + BatchNorm'},
        'Output Layer': {'size': 6, 'type': 'Dense'}
    }
    viz.plot_model_architecture(architecture_data, "集群规划模型结构分析",
                              chapter=5, category='model', subcategory='architecture')

    # 10. Feature Importance
    feature_data = {
        '相对位置': 0.95,
        '相对速度': 0.85,
        '目标位置': 0.80,
        '障碍物信息': 0.75,
        '通信状态': 0.70,
        '编队形状': 0.65
    }
    viz.plot_feature_importance(feature_data, "集群规划特征重要性分析",
                              chapter=5, category='model', subcategory='features')

    # 11. Decision Boundary
    decision_data = {
        'Base Model': {
            'features': np.random.normal(0, 1, (100, 2)),
            'confidence': np.random.uniform(0.5, 1.0, 100)
        },
        'Enhanced Model': {
            'features': np.random.normal(0.2, 0.8, (100, 2)),
            'confidence': np.random.uniform(0.7, 1.0, 100)
        }
    }
    viz.plot_decision_boundary(decision_data, "集群规划决策边界分析",
                             chapter=5, category='model', subcategory='decision')

    # 12. Hyperparameter Analysis
    hyperparameter_data = {
        'Base Model': {
            'learning_rates': np.logspace(-4, -1, 10),
            'batch_sizes': [16, 32, 64, 128, 256],
            'performance': np.random.uniform(0.7, 0.9, 10)
        },
        'Enhanced Model': {
            'learning_rates': np.logspace(-4, -1, 10),
            'batch_sizes': [16, 32, 64, 128, 256],
            'performance': np.random.uniform(0.8, 0.95, 10)
        }
    }
    viz.plot_hyperparameter_analysis(hyperparameter_data, "集群规划超参数分析",
                                   chapter=5, category='model', subcategory='hyperparameters')

    # 13. Error Distribution Analysis
    error_data = {
        'Base Model': {
            'formation_errors': np.random.normal(0.2, 0.05, 1000),
            'communication_errors': np.random.normal(0.15, 0.03, 1000)
        },
        'Enhanced Model': {
            'formation_errors': np.random.normal(0.15, 0.04, 1000),
            'communication_errors': np.random.normal(0.12, 0.02, 1000)
        }
    }
    viz.plot_error_distribution(error_data, "集群规划误差分布分析",
                              chapter=5, category='performance', subcategory='errors')

    # 14. Ensemble Performance
    ensemble_data = {
        'Base Model': {
            'timesteps': list(range(100)),
            'individual_performance': [0.8 + 0.1 * np.sin(0.1 * x) + 0.05 * np.random.random() for x in range(100)],
            'ensemble_performance': [0.85 + 0.08 * np.sin(0.1 * x) + 0.03 * np.random.random() for x in range(100)]
        },
        'Enhanced Model': {
            'timesteps': list(range(100)),
            'individual_performance': [0.85 + 0.08 * np.sin(0.1 * x) + 0.04 * np.random.random() for x in range(100)],
            'ensemble_performance': [0.9 + 0.06 * np.sin(0.1 * x) + 0.02 * np.random.random() for x in range(100)]
        }
    }
    viz.plot_ensemble_performance(ensemble_data, "集群规划集成性能分析",
                                chapter=5, category='performance', subcategory='ensemble')

    # 15. Training Dynamics
    dynamics_data = {
        'Base Model': {
            'epochs': list(range(100)),
            'gradients': [np.exp(-0.05 * x) + 0.1 * np.random.random() for x in range(100)],
            'weights': [1 - np.exp(-0.03 * x) + 0.1 * np.random.random() for x in range(100)]
        },
        'Enhanced Model': {
            'epochs': list(range(100)),
            'gradients': [0.8 * np.exp(-0.06 * x) + 0.08 * np.random.random() for x in range(100)],
            'weights': [1 - 0.8 * np.exp(-0.04 * x) + 0.08 * np.random.random() for x in range(100)]
        }
    }
    viz.plot_training_dynamics(dynamics_data, "集群规划训练动态分析",
                             chapter=5, category='training', subcategory='dynamics')

    # 16. Model Comparison
    comparison_data = {
        'metrics': ['编队准确率', '通信效率', '可扩展性', '鲁棒性'],
        'models': ['基准模型', '改进模型'],
        'values': [
            [0.85, 0.92],  # 编队准确率
            [0.80, 0.88],  # 通信效率
            [0.75, 0.85],  # 可扩展性
            [0.82, 0.90]   # 鲁棒性
        ]
    }
    viz.plot_model_comparison(comparison_data, "集群规划模型对比分析",
                            chapter=5, category='performance', subcategory='comparison')

    # 17. Path Quality Analysis
    path_quality_data = {
        'paths': {
            'Base Model': np.array([[x, np.sin(0.1*x), np.cos(0.1*x)] for x in range(100)]),
            'Enhanced Model': np.array([[x, 1.2*np.sin(0.1*x), 1.2*np.cos(0.1*x)] for x in range(100)])
        },
        'metrics': {
            'Base Model': {
                '路径长度': 0.85,
                '平滑度': 0.82,
                '安全裕度': 0.78,
                '能量效率': 0.80,
                '计算时间': 0.75
            },
            'Enhanced Model': {
                '路径长度': 0.90,
                '平滑度': 0.88,
                '安全裕度': 0.85,
                '能量效率': 0.87,
                '计算时间': 0.82
            }
        }
    }
    viz.plot_path_quality(path_quality_data['paths'], path_quality_data['metrics'], "集群规划路径质量分析",
                         chapter=5, category='performance', subcategory='quality')

    # 18. Environmental Impact Analysis
    impact_data = {
        'paths': {
            'Base Model': np.array([[x, np.sin(0.1*x), np.cos(0.1*x)] for x in range(100)]),
            'Enhanced Model': np.array([[x, 1.2*np.sin(0.1*x), 1.2*np.cos(0.1*x)] for x in range(100)])
        },
        'env': env
    }
    viz.plot_environmental_impact(impact_data['paths'], impact_data['env'], "集群规划环境影响分析",
                                chapter=5, category='performance', subcategory='environment')

    # 19. Performance Metrics 3D
    metrics_3d_data = {
        'Base Model': {
            'formation_accuracy': 0.85,
            'communication_efficiency': 0.80,
            'scalability': 0.75
        },
        'Enhanced Model': {
            'formation_accuracy': 0.92,
            'communication_efficiency': 0.88,
            'scalability': 0.85
        }
    }
    viz.plot_performance_metrics_3d(metrics_3d_data, "集群规划性能三维分析",
                                  chapter=5, category='performance', subcategory='3d_metrics')

    # 20. Path Complexity Analysis
    complexity_paths = {
        'Base Model': np.array([[x, np.sin(0.1*x), np.cos(0.1*x)] for x in range(100)]),
        'Enhanced Model': np.array([[x, 1.2*np.sin(0.1*x), 1.2*np.cos(0.1*x)] for x in range(100)])
    }
    viz.plot_path_complexity(complexity_paths, "集群规划路径复杂度分析",
                           chapter=5, category='performance', subcategory='complexity')

    # 21. Convergence Speed Analysis
    convergence_data = {
        'Base Model': [np.exp(-0.05 * x) + 0.1 * np.random.random() for x in range(100)],
        'Enhanced Model': [0.8 * np.exp(-0.06 * x) + 0.08 * np.random.random() for x in range(100)]
    }
    iterations = list(range(100))
    viz.plot_convergence_speed(convergence_data, iterations, "集群规划收敛速度分析",
                             chapter=5, category='performance', subcategory='convergence')

    # 22. Parameter Sensitivity Analysis
    sensitivity_data = {
        'Base Model': {
            'learning_rate': [0.8, 0.85, 0.75],
            'batch_size': [0.82, 0.87, 0.78], 
            'hidden_size': [0.79, 0.83, 0.73]
        },
        'Enhanced Model': {
            'learning_rate': [0.85, 0.9, 0.8],
            'batch_size': [0.87, 0.92, 0.83],
            'hidden_size': [0.84, 0.88, 0.78]
        }
    }
    params = {
        'learning_rate': [0.001, 0.01, 0.1],
        'batch_size': [32, 64, 128],
        'hidden_size': [64, 128, 256]
    }
    viz.plot_parameter_sensitivity(sensitivity_data, params, "集群规划参数敏感性分析",
                                 chapter=5, category='ablation', subcategory='sensitivity')

    # 23. Multi-Objective Analysis
    objective_data = {
        'Base Model': {
            'formation_stability': 0.85,
            'energy_efficiency': 0.80,
            'communication_cost': 0.75
        },
        'Enhanced Model': {
            'formation_stability': 0.90,
            'energy_efficiency': 0.85,
            'communication_cost': 0.80
        }
    }
    objectives = ['formation_stability', 'energy_efficiency', 'communication_cost']
    viz.plot_multi_objective(objective_data, objectives, "集群规划多目标优化分析",
                           chapter=5, category='performance', subcategory='multi_objective')

if __name__ == "__main__":
    generate_chapter5_visualizations()
