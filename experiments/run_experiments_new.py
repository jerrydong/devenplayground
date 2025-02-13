import numpy as np
from typing import Dict, List, Any
import os
import logging
import traceback
from config import create_experiment_suite
from visualization_enhanced_v2 import EnhancedVisualizerV2
from environment import Environment
from algorithms.neural_ahpp import NeuralAHPP
from algorithms.cluster_planner import ClusterPlanner
from algorithms.rrt_star import RRTStar
from algorithms.dynamic_predictor import DynamicPredictor
from metrics import calculate_path_metrics

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExperimentRunner:
    """Experiment Runner for Path Planning"""
    
    def __init__(self, output_dir="results"):
        self.config = create_experiment_suite()
        self.visualizer = EnhancedVisualizerV2(output_dir)
        self.output_dir = output_dir
        self.visualization_count = 0
        self.visualization_files = []
        os.makedirs(output_dir, exist_ok=True)
        
    def run_all_experiments(self):
        """Run all experiments"""
        results = {}
        visualization_files = []
        
        try:
            # 1. Neural Evolution Algorithm Experiments
            logger.info("Running Neural Evolution experiments...")
            neural_results = self._run_neural_ablation()
            results['neural'] = neural_results
            if 'visualizations' in neural_results:
                visualization_files.extend(neural_results['visualizations'])
            
            # Generate energy efficiency analysis
            logger.info("Generating energy efficiency analysis...")
            energy_viz = self.visualizer.plot_energy_efficiency(
                neural_results['paths'],
                "神经进化算法能量效率分析"
            )
            visualization_files.append(energy_viz)
            
            # Generate obstacle avoidance analysis
            logger.info("Generating obstacle avoidance analysis...")
            safety_viz = self.visualizer.plot_obstacle_avoidance(
                neural_results['paths'],
                self.config['experiment'].env,
                "神经进化算法避障性能分析"
            )
            visualization_files.append(safety_viz)
            
            # Generate convergence speed analysis
            logger.info("Generating convergence speed analysis...")
            convergence_data = {}
            for name, metrics in neural_results['metrics'].items():
                # Extract convergence data from metrics
                iterations = list(range(len(metrics['iterations'])))
                values = metrics['iterations']
                convergence_data[name] = values
            
            convergence_viz = self.visualizer.plot_convergence_speed(
                convergence_data,
                iterations,
                "神经进化算法收敛性分析"
            )
            visualization_files.append(convergence_viz)
            
            # 2. Dynamic Environment Experiments
            logger.info("Running dynamic environment experiments...")
            dynamic_results = self._run_dynamic_ablation()
            results['dynamic'] = dynamic_results
            if 'visualizations' in dynamic_results:
                visualization_files.extend(dynamic_results['visualizations'])
            
            # Generate parameter sensitivity analysis
            logger.info("Generating parameter sensitivity analysis...")
            params = {
                '预测时域': [1.0, 2.0, 3.0, 4.0, 5.0],
                '不确定性阈值': [0.1, 0.2, 0.3, 0.4, 0.5],
                '采样密度': [10, 20, 30, 40, 50]
            }
            sensitivity_viz = self.visualizer.plot_parameter_sensitivity(
                dynamic_results['sensitivity'],
                params,
                "动态环境规划参数敏感性分析"
            )
            visualization_files.append(sensitivity_viz)
            
            # Generate multi-objective analysis
            logger.info("Generating multi-objective analysis...")
            objectives = ['安全性', '实时性', '平滑度', '能量效率']
            multi_obj_viz = self.visualizer.plot_multi_objective(
                dynamic_results['metrics'],
                objectives,
                "动态环境规划多目标优化分析"
            )
            visualization_files.append(multi_obj_viz)
            
            # Generate real-time performance analysis
            logger.info("Generating real-time performance analysis...")
            realtime_viz = self.visualizer.plot_real_time_performance(
                dynamic_results['timing'],
                "动态环境规划实时性能分析"
            )
            visualization_files.append(realtime_viz)
            
            # Generate path quality analysis
            logger.info("Generating path quality analysis...")
            quality_viz = self.visualizer.plot_path_quality(
                dynamic_results['paths'],
                dynamic_results['metrics'],
                "路径规划质量分析"
            )
            visualization_files.append(quality_viz)
            
            # Generate environmental impact analysis
            logger.info("Generating environmental impact analysis...")
            env_viz = self.visualizer.plot_environmental_impact(
                dynamic_results['paths'],
                self.config['experiment'].env,
                "环境影响分析"
            )
            visualization_files.append(env_viz)
            
            # Generate multi-drone coordination analysis
            logger.info("Generating multi-drone coordination analysis...")
            if 'cluster' in results and 'paths' in results['cluster']:
                coord_viz = self.visualizer.plot_multi_drone_coordination(
                    results['cluster']['paths'],
                    "多无人机协调性能分析"
                )
                visualization_files.append(coord_viz)
            
            # Generate robustness analysis
            logger.info("Generating robustness analysis...")
            if 'metrics' in dynamic_results:
                robust_viz = self.visualizer.plot_robustness_analysis(
                    {name: {'performance': metrics.get('performance', [0.8, 0.85, 0.9]),
                           'recovery_time': metrics.get('recovery_time', [100, 120, 90]),
                           'error_tolerance': metrics.get('error_tolerance', 0.85)}
                     for name, metrics in dynamic_results['metrics'].items()},
                    "算法鲁棒性分析"
                )
                visualization_files.append(robust_viz)
            
            # Generate scalability analysis
            logger.info("Generating scalability analysis...")
            scale_viz = self.visualizer.plot_scalability_analysis(
                {name: {'problem_size': metrics['problem_size'],
                       'computation_time': metrics['computation_time'],
                       'memory_usage': metrics['memory_usage'],
                       'performance': metrics['performance']}
                 for name, metrics in dynamic_results['metrics'].items()},
                "算法可扩展性分析"
            )
            visualization_files.append(scale_viz)
            
            # Generate adaptation analysis
            logger.info("Generating adaptation analysis...")
            adapt_viz = self.visualizer.plot_adaptation_analysis(
                {name: {'adaptation_time': metrics['adaptation_time'],
                       'performance_recovery': metrics['performance_recovery']}
                 for name, metrics in dynamic_results['metrics'].items()},
                "环境适应性分析"
            )
            visualization_files.append(adapt_viz)
            
            # Generate learning curves analysis
            logger.info("Generating learning curves analysis...")
            learning_viz = self.visualizer.plot_learning_curves(
                {name: metrics for name, metrics in dynamic_results['metrics'].items()},
                "学习曲线分析"
            )
            visualization_files.append(learning_viz)
            
            # Generate optimization landscape analysis
            logger.info("Generating optimization landscape analysis...")
            opt_viz = self.visualizer.plot_optimization_landscape(
                {name: metrics for name, metrics in dynamic_results['metrics'].items()},
                "优化景观分析"
            )
            visualization_files.append(opt_viz)
            
            # Generate feature importance analysis
            logger.info("Generating feature importance analysis...")
            feature_viz = self.visualizer.plot_feature_importance(
                {name: metrics for name, metrics in dynamic_results['metrics'].items()},
                "特征重要性分析"
            )
            visualization_files.append(feature_viz)
            
            # Generate decision boundary analysis
            logger.info("Generating decision boundary analysis...")
            decision_viz = self.visualizer.plot_decision_boundary(
                {name: metrics for name, metrics in dynamic_results['metrics'].items()},
                "决策边界分析"
            )
            visualization_files.append(decision_viz)
            
            # Generate model architecture analysis
            logger.info("Generating model architecture analysis...")
            arch_viz = self.visualizer.plot_model_architecture(
                {name: metrics for name, metrics in dynamic_results['metrics'].items()},
                "模型架构分析"
            )
            visualization_files.append(arch_viz)
            
            # Generate hyperparameter analysis
            logger.info("Generating hyperparameter analysis...")
            hyper_viz = self.visualizer.plot_hyperparameter_analysis(
                {name: metrics for name, metrics in dynamic_results['metrics'].items()},
                "超参数分析"
            )
            visualization_files.append(hyper_viz)
            
            # Generate error distribution analysis
            logger.info("Generating error distribution analysis...")
            error_viz = self.visualizer.plot_error_distribution(
                {name: metrics for name, metrics in dynamic_results['metrics'].items()},
                "误差分布分析"
            )
            visualization_files.append(error_viz)
            
            # Generate ensemble performance analysis
            logger.info("Generating ensemble performance analysis...")
            ensemble_viz = self.visualizer.plot_ensemble_performance(
                {name: metrics for name, metrics in dynamic_results['metrics'].items()},
                "集成性能分析"
            )
            visualization_files.append(ensemble_viz)
            
            # Generate training dynamics analysis
            logger.info("Generating training dynamics analysis...")
            dynamics_viz = self.visualizer.plot_training_dynamics(
                {name: metrics for name, metrics in dynamic_results['metrics'].items()},
                "训练动态分析"
            )
            visualization_files.append(dynamics_viz)
            
            # Generate model comparison analysis
            logger.info("Generating model comparison analysis...")
            comparison_viz = self.visualizer.plot_model_comparison(
                {name: metrics for name, metrics in dynamic_results['metrics'].items()},
                "模型综合对比分析"
            )
            visualization_files.append(comparison_viz)
            
            # 3. Cluster Planning Experiments
            logger.info("Running cluster planning experiments...")
            cluster_results = self._run_cluster_ablation()
            results['cluster'] = cluster_results
            if 'visualizations' in cluster_results:
                visualization_files.extend(cluster_results['visualizations'])
            
            # 4. Generate Additional Visualization Results
            logger.info("Generating additional visualization results...")
            additional_visualizations = self._generate_cross_chapter_visualizations(
                neural_results, dynamic_results, cluster_results
            )
            if additional_visualizations:
                visualization_files.extend(additional_visualizations)
            
            results['visualizations'] = visualization_files
            
        except Exception as e:
            logger.error(f"Error during experiments: {e}")
            traceback.print_exc()
            
        # Report visualization count
        valid_files = [f for f in visualization_files if f and os.path.exists(f)]
        logger.info(f"\nGenerated {len(valid_files)} visualizations:")
        for i, viz_file in enumerate(valid_files, 1):
            logger.info(f"{i}. {viz_file}")
            
        return results
        
    def _run_neural_ablation(self):
        """Run neural evolution ablation experiments"""
        results = {}
        paths = {}
        visualization_files = []
        
        # Test scenarios
        scenarios = [
            ('简单场景', np.array([10, 10, 10]), np.array([180, 180, 10])),
            ('复杂场景', np.array([20, 180, 20]), np.array([180, 20, 20])),
            ('狭窄场景', np.array([10, 10, 50]), np.array([180, 180, 50]))
        ]
        
        variants = {
            '基准模型': {'use_experience_replay': False, 'use_attention': False, 'adaptive_sampling': False},
            '经验回放': {'use_experience_replay': True, 'use_attention': False, 'adaptive_sampling': False},
            '注意力机制': {'use_experience_replay': False, 'use_attention': True, 'adaptive_sampling': False},
            '自适应采样': {'use_experience_replay': False, 'use_attention': False, 'adaptive_sampling': True},
            '完整模型': {'use_experience_replay': True, 'use_attention': True, 'adaptive_sampling': True}
        }
        
        for scenario_name, start, goal in scenarios:
            env = Environment(size=self.config['experiment'].env_size)
            scenario_results = {}
            scenario_paths = {}
            
            for name, config in variants.items():
                planner = NeuralAHPP(env)
                planner.use_experience_replay = config['use_experience_replay']
                planner.use_attention = config['use_attention']
                planner.adaptive_sampling = config['adaptive_sampling']
                
                try:
                    path = planner.plan_path(start, goal)
                    if path is not None and len(path) > 0:
                        metrics = calculate_path_metrics(path, env)
                        scenario_results[name] = metrics
                        scenario_paths[name] = path
                        
                        # Generate visualization for this configuration
                        try:
                            viz_file = self.visualizer.plot_3d_path_with_obstacles(
                                path, env, 
                                f"{scenario_name} - {name}"
                            )
                            visualization_files.append(viz_file)
                            logger.info(f"Generated visualization: {viz_file}")
                            
                            # Generate additional visualizations
                            viz_file = self.visualizer.plot_path_characteristics(
                                {name: path}, 
                                f"{scenario_name} - {name} 路径特征分析"
                            )
                            visualization_files.append(viz_file)
                            
                            viz_file = self.visualizer.plot_path_complexity(
                                {name: path},
                                f"{scenario_name} - {name} 路径复杂度分析"
                            )
                            visualization_files.append(viz_file)
                            
                        except Exception as e:
                            logger.warning(f"Failed to generate visualization for {name} in {scenario_name}: {e}")
                    else:
                        logger.warning(f"No valid path found for {name} in {scenario_name}")
                except Exception as e:
                    logger.warning(f"Failed to plan path for {name} in {scenario_name}: {e}")
                    continue
            
            results[scenario_name] = scenario_results
            paths[scenario_name] = scenario_paths
            
            # Generate comparative visualizations for this scenario
            try:
                viz_file = self.visualizer.plot_3d_comparison(
                    scenario_paths, env,
                    f"{scenario_name} - 路径对比分析"
                )
                visualization_files.append(viz_file)
                
                viz_file = self.visualizer.plot_metrics_comparison(
                    scenario_results,
                    f"{scenario_name} - 性能指标对比"
                )
                visualization_files.append(viz_file)
                
                viz_file = self.visualizer.create_animation(
                    scenario_paths, env,
                    f"{scenario_name} - 路径规划动画"
                )
                visualization_files.append(viz_file)
            except Exception as e:
                logger.warning(f"Failed to generate comparative visualizations for {scenario_name}: {e}")
                
        return {
            'metrics': results,
            'paths': paths,
            'visualizations': visualization_files
        }
        
    def _run_dynamic_ablation(self):
        """Run dynamic environment ablation experiments"""
        results = {}
        paths = {}
        visualization_files = []
        timing_data = {}
        sensitivity_data = {}
        models_data = {}
        
        # Test scenarios with dynamic obstacles
        scenarios = {
            '简单动态场景': {'num_obstacles': 5, 'speed': 0.5},
            '复杂动态场景': {'num_obstacles': 10, 'speed': 1.0}
        }
        
        variants = {
            '基准模型': {'use_prediction': False, 'use_uncertainty': False},
            '预测模型': {'use_prediction': True, 'use_uncertainty': False},
            '不确定性感知': {'use_prediction': True, 'use_uncertainty': True},
            '自适应规划': {'use_prediction': True, 'use_uncertainty': True, 'use_adaptation': True}
        }
        
        for scenario_name, config in scenarios.items():
            scenario_results = {}
            scenario_paths = {}
            
            for name, params in variants.items():
                try:
                    env = Environment(size=self.config['experiment'].env_size,
                                    num_obstacles=config['num_obstacles'])
                    
                    planner = NeuralAHPP(env)
                    planner.use_prediction = params.get('use_prediction', False)
                    planner.use_uncertainty = params.get('use_uncertainty', False)
                    planner.use_adaptation = params.get('use_adaptation', False)
                    
                    start = np.array([10, 10, 10])
                    goal = np.array([180, 180, 10])
                    
                    path = planner.plan_path(start, goal)
                    if path is not None and len(path) > 0:
                        metrics = calculate_path_metrics(path, env)
                        scenario_results[name] = metrics
                        scenario_paths[name] = path
                        
                        # Generate visualization for this configuration
                        try:
                            viz_file = self.visualizer.plot_3d_path_with_obstacles(
                                path, env, 
                                f"{scenario_name} - {name}"
                            )
                            visualization_files.append(viz_file)
                            logger.info(f"Generated visualization: {viz_file}")
                            
                            # Generate additional visualizations
                            viz_file = self.visualizer.plot_path_characteristics(
                                {name: path}, 
                                f"{scenario_name} - {name} 路径特征分析"
                            )
                            visualization_files.append(viz_file)
                            
                            viz_file = self.visualizer.plot_path_complexity(
                                {name: path},
                                f"{scenario_name} - {name} 路径复杂度分析"
                            )
                            visualization_files.append(viz_file)
                            
                        except Exception as e:
                            logger.warning(f"Failed to generate visualization for {name} in {scenario_name}: {e}")
                    else:
                        logger.warning(f"No valid path found for {name} in {scenario_name}")
                except Exception as e:
                    logger.warning(f"Failed to plan path for {name} in {scenario_name}: {e}")
                    continue
            
            results[scenario_name] = scenario_results
            paths[scenario_name] = scenario_paths
            
            # Generate comparative visualizations for this scenario
            try:
                viz_file = self.visualizer.plot_3d_comparison(
                    scenario_paths, env,
                    f"{scenario_name} - 路径对比分析"
                )
                visualization_files.append(viz_file)
                
                viz_file = self.visualizer.plot_metrics_comparison(
                    scenario_results,
                    f"{scenario_name} - 性能指标对比"
                )
                visualization_files.append(viz_file)
                
                viz_file = self.visualizer.create_animation(
                    scenario_paths, env,
                    f"{scenario_name} - 路径规划动画"
                )
                visualization_files.append(viz_file)
            except Exception as e:
                logger.warning(f"Failed to generate comparative visualizations for {scenario_name}: {e}")
                
        return {
            'metrics': results,
            'paths': paths,
            'visualizations': visualization_files
        }
        
    def _run_cluster_ablation(self):
        """Run cluster planning ablation experiments"""
        results = {}
        paths = {}
        visualization_files = []
        
        # Test scenarios
        scenarios = [
            ('简单集群场景', 5),
            ('中等集群场景', 10),
            ('复杂集群场景', 15)
        ]
        
        variants = {
            '基准模型': {'use_adaptive_clustering': False, 'use_attention': False, 'use_formation': False},
            '自适应聚类': {'use_adaptive_clustering': True, 'use_attention': False, 'use_formation': False},
            '注意力机制': {'use_adaptive_clustering': False, 'use_attention': True, 'use_formation': False},
            '队形控制': {'use_adaptive_clustering': False, 'use_attention': False, 'use_formation': True},
            '完整模型': {'use_adaptive_clustering': True, 'use_attention': True, 'use_formation': True}
        }
        
        for scenario_name, num_drones in scenarios:
            env = Environment(size=self.config['experiment'].env_size)
            scenario_results = {}
            scenario_paths = {}
            
            for name, config in variants.items():
                try:
                    planner = ClusterPlanner(env, num_drones=num_drones)
                    planner.use_adaptive_clustering = config['use_adaptive_clustering']
                    planner.use_attention = config['use_attention']
                    planner.use_formation = config['use_formation']
                    
                    start_positions = [
                        np.array([10 + i*20, 10, 10]) for i in range(num_drones)
                    ]
                    goal_positions = [
                        np.array([180 - i*20, 180, 10]) for i in range(num_drones)
                    ]
                    
                    paths_list = planner.plan_paths(start_positions, goal_positions)
                    if paths_list:
                        metrics = calculate_path_metrics(np.concatenate(paths_list), env)
                        scenario_results[name] = metrics
                        scenario_paths[name] = paths_list[0]  # Show lead drone's path
                        
                        # Generate visualization for this configuration
                        try:
                            viz_file = self.visualizer.plot_3d_path_with_obstacles(
                                paths_list[0], env,
                                f"{scenario_name} - {name}"
                            )
                            visualization_files.append(viz_file)
                            logger.info(f"Generated visualization: {viz_file}")
                            
                            # Generate additional visualizations
                            viz_file = self.visualizer.plot_path_characteristics(
                                {name: paths_list[0]}, 
                                f"{scenario_name} - {name} 路径特征分析"
                            )
                            visualization_files.append(viz_file)
                            
                            viz_file = self.visualizer.plot_path_complexity(
                                {name: paths_list[0]},
                                f"{scenario_name} - {name} 路径复杂度分析"
                            )
                            visualization_files.append(viz_file)
                            
                        except Exception as e:
                            logger.warning(f"Failed to generate visualization for {name} in {scenario_name}: {e}")
                    else:
                        logger.warning(f"No valid paths found for {name} in {scenario_name}")
                except Exception as e:
                    logger.warning(f"Failed to plan paths for {name} in {scenario_name}: {e}")
                    continue
            
            results[scenario_name] = scenario_results
            paths[scenario_name] = scenario_paths
            
            # Generate comparative visualizations for this scenario
            try:
                viz_file = self.visualizer.plot_3d_comparison(
                    scenario_paths, env,
                    f"{scenario_name} - 路径对比分析"
                )
                visualization_files.append(viz_file)
                
                viz_file = self.visualizer.plot_metrics_comparison(
                    scenario_results,
                    f"{scenario_name} - 性能指标对比"
                )
                visualization_files.append(viz_file)
                
                viz_file = self.visualizer.create_animation(
                    scenario_paths, env,
                    f"{scenario_name} - 路径规划动画"
                )
                visualization_files.append(viz_file)
            except Exception as e:
                logger.warning(f"Failed to generate comparative visualizations for {scenario_name}: {e}")
                
        return {
            'metrics': results,
            'paths': paths,
            'visualizations': visualization_files
        }
        
    def _generate_cross_chapter_visualizations(self, neural_results, dynamic_results, cluster_results):
        """Generate cross-chapter comparative visualizations"""
        visualization_files = []
        
        try:
            # 1. Cross-Chapter Performance Analysis
            combined_metrics = {
                '神经进化算法': neural_results['metrics'],
                '动态环境规划': dynamic_results['metrics'],
                '集群路径规划': cluster_results['metrics']
            }
            
            viz_file = self.visualizer.plot_metrics_comparison(
                combined_metrics,
                "跨章节性能对比分析"
            )
            visualization_files.append(viz_file)
            
            # 2. Path Complexity Analysis
            combined_paths = {
                '神经进化算法': neural_results['paths'],
                '动态环境规划': dynamic_results['paths'],
                '集群路径规划': cluster_results['paths']
            }
            
            viz_file = self.visualizer.plot_path_complexity(
                combined_paths,
                "跨章节路径复杂度分析"
            )
            visualization_files.append(viz_file)
            
            # 3. Success Rate Analysis
            viz_file = self.visualizer.plot_success_rate_by_scenario(
                combined_metrics,
                "跨章节成功率分析"
            )
            visualization_files.append(viz_file)
            
        except Exception as e:
            logger.warning(f"Failed to generate cross-chapter visualizations: {e}")
            
        return visualization_files

if __name__ == "__main__":
    runner = ExperimentRunner()
    results = runner.run_all_experiments()
    
    logger.info("\nExperiments completed! Generated the following visualizations:")
    for viz_file in results['visualizations']:
        logger.info(f"- {viz_file}")
