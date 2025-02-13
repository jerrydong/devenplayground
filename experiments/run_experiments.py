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

# Configure matplotlib for Chinese characters
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ASCII Labels for consistent display
EXPERIMENT_LABELS = {
    'neural_evolution': 'Neural Evolution Algorithm',
    'dynamic_environment': 'Dynamic Environment Planning',
    'cluster_planning': 'Cluster Path Planning',
    'ablation': 'Ablation Study',
    'comparison': 'Algorithm Comparison',
    'scenarios': 'Scenario Analysis'
}

class ExperimentRunner:
    """Experiment Runner for Path Planning"""
    
    def __init__(self, output_dir="results"):
        self.config = create_experiment_suite()
        self.visualizer = EnhancedVisualizerV2(output_dir)
        self.output_dir = output_dir
        self.visualization_count = 0
        self.visualization_files = []
        os.makedirs(output_dir, exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(os.path.join(output_dir, 'experiment.log'))
            ]
        )
        
    def track_visualization(self, filepath: str) -> str:
        """Track visualization and return filepath"""
        if filepath and os.path.exists(filepath):
            self.visualization_count += 1
            logger.info(f"Generated visualization {self.visualization_count}: {filepath}")
        return filepath
        
    def run_all_experiments(self):
        """Run all experiments"""
        results = {}
        visualization_files = []
        
        try:
            # 1. Neural Evolution Algorithm Experiments
            logger.info("Running Neural Evolution experiments...")
            neural_results = self.run_neural_evolution_experiments()
            results['neural'] = neural_results
            if isinstance(neural_results, dict) and 'visualizations' in neural_results:
                visualization_files.extend(neural_results['visualizations'])
            
            # 2. Dynamic Environment Experiments
            logger.info("Running dynamic environment experiments...")
            dynamic_results = self.run_dynamic_experiments()
            results['dynamic'] = dynamic_results
            if isinstance(dynamic_results, dict) and 'visualizations' in dynamic_results:
                visualization_files.extend(dynamic_results['visualizations'])
            
            # 3. Cluster Planning Experiments
            logger.info("Running cluster planning experiments...")
            cluster_results = self.run_cluster_experiments()
            results['cluster'] = cluster_results
            if isinstance(cluster_results, dict) and 'visualizations' in cluster_results:
                visualization_files.extend(cluster_results['visualizations'])
            
            # 4. Generate Additional Visualization Results
            logger.info("Generating additional visualization results...")
            additional_visualizations = self.generate_visualizations(
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
        
    def run_neural_evolution_experiments(self):
        """Run neural evolution algorithm experiments"""
        results = {
            'ablation': self._run_neural_ablation(),
            'comparison': self._run_neural_comparison(),
            'scenarios': self._run_neural_scenarios()
        }
        
        # Track visualization count
        logger.info(f"Total visualizations generated: {self.visualization_count}")
        return results
        
    def run_dynamic_experiments(self):
        """Run dynamic environment experiments"""
        results = {
            'ablation': self._run_dynamic_ablation(),
            'comparison': self._run_dynamic_comparison(),
            'scenarios': self._run_dynamic_scenarios()
        }
        logger.info(f"Total visualizations generated: {self.visualization_count}")
        return results
        
    def run_cluster_experiments(self):
        """Run cluster planning experiments"""
        results = {
            'ablation': self._run_cluster_ablation(),
            'comparison': self._run_cluster_comparison(),
            'scenarios': self._run_cluster_scenarios()
        }
        logger.info(f"Total visualizations generated: {self.visualization_count}")
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
            
            # Generate comparison visualization for this scenario
            viz_file = self.track_visualization(
                self.visualizer.plot_3d_comparison(
                    scenario_paths, env,
                    f"Neural Evolution Ablation Study - {scenario_name}"
                )
            )
            
            # Generate metrics comparison
            viz_file = self.track_visualization(
                self.visualizer.plot_metrics_comparison(
                    scenario_results,
                    f"Neural Evolution Performance Metrics - {scenario_name}"
                )
            )
            
            # Generate animation
            viz_file = self.track_visualization(
                self.visualizer.create_animation(
                    scenario_paths, env,
                    f"Neural Evolution Path Planning - {scenario_name}"
                )
            )
            
            # Generate additional visualizations
            viz_file = self.track_visualization(
                self.visualizer.plot_violin(
                    {name: [m['time'] for m in metrics.values()] 
                     for name, metrics in scenario_results.items()},
                    f"Neural Evolution Time Distribution - {scenario_name}"
                )
            )
            
            viz_file = self.track_visualization(
                self.visualizer.plot_box(
                    {name: [m['safety'] for m in metrics.values()]
                     for name, metrics in scenario_results.items()},
                    f"Neural Evolution Safety Distribution - {scenario_name}"
                )
            )
            
            viz_file = self.track_visualization(
                self.visualizer.plot_parallel_coordinates(
                    {name: metrics for name, metrics in scenario_results.items()},
                    f"Neural Evolution Multi-Metric Analysis - {scenario_name}"
                )
            )
            
            # Generate joint distribution plots
            for name, metrics in scenario_results.items():
                times = [m['time'] for m in metrics.values()]
                safety = [m['safety'] for m in metrics.values()]
                viz_file = self.track_visualization(
                    self.visualizer.plot_joint_distribution(
                        times, safety,
                        "Time", "Safety",
                        f"Neural Evolution Time-Safety Distribution - {name} - {scenario_name}"
                    )
                )
        
        return results
        
    def _run_neural_comparison(self):
        """Run neural evolution comparison experiments"""
        env = Environment(size=self.config['experiment'].env_size)
        start = np.array([10, 10, 10])
        goal = np.array([180, 180, 10])
        
        results = {}
        # Neural AHPP
        planner = NeuralAHPP(env)
        path = planner.plan_path(start, goal)
        results['Neural AHPP'] = calculate_path_metrics(path, env)
        
        # RRT*
        rrt = RRTStar(env)
        path = rrt.plan(start, goal)
        results['RRT*'] = calculate_path_metrics(path, env)
        
        return results
        
    def _run_neural_scenarios(self):
        """Run neural evolution scenario experiments"""
        results = {}
        for name, scenario in self.config['experiment'].scenarios.items():
            env = Environment(size=self.config['experiment'].env_size,
                            num_obstacles=scenario['num_obstacles'])
            
            start = np.array([10, 10, 10])
            goal = np.array([180, 180, 10])
            
            planner = NeuralAHPP(env)
            path = planner.plan_path(start, goal)
            results[name] = calculate_path_metrics(path, env)
            
        return results
        
    def _run_dynamic_ablation(self):
        """Run dynamic environment ablation experiments"""
        logger.info("Running dynamic environment ablation experiments...")
        results = {}
        paths = {}
        
        # Test scenarios with dynamic obstacles
        scenarios = {
            'simple_dynamic': {'num_obstacles': 5, 'speed': 0.5},
            'complex_dynamic': {'num_obstacles': 10, 'speed': 1.0}
        }
        
        for scenario_name, config in scenarios.items():
            scenario_results = {}
            scenario_paths = {}
            
            # Run baseline and variants
            variants = {
                'baseline': {'use_prediction': False, 'use_uncertainty': False},
                'with_prediction': {'use_prediction': True, 'use_uncertainty': False},
                'with_uncertainty': {'use_prediction': True, 'use_uncertainty': True},
                'full_model': {'use_prediction': True, 'use_uncertainty': True, 'use_adaptation': True}
            }
            
            for name, params in variants.items():
                # Run experiment...
                try:
                    # Create environment for this variant
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
                except Exception as e:
                    logger.warning(f"Failed to plan path for {name}: {e}")
                    scenario_results[name] = {}
                    scenario_paths[name] = []
            
            # Create environment for visualization
            env = Environment(size=self.config['experiment'].env_size,
                            num_obstacles=config['num_obstacles'])
            
            # Generate visualizations
            viz_file = self.track_visualization(
                self.visualizer.plot_3d_comparison(
                    scenario_paths, env,
                    f"Dynamic Path Planning Comparison - {scenario_name}"
                )
            )
            
            viz_file = self.track_visualization(
                self.visualizer.plot_metrics_comparison(
                    scenario_results,
                    f"Dynamic Planning Performance - {scenario_name}"
                )
            )
            
            viz_file = self.track_visualization(
                self.visualizer.plot_violin(
                    {name: [m['time'] for m in metrics.values()] 
                     for name, metrics in scenario_results.items()},
                    f"Dynamic Planning Time Distribution - {scenario_name}"
                )
            )
            
            viz_file = self.track_visualization(
                self.visualizer.plot_box(
                    {name: [m['safety'] for m in metrics.values()]
                     for name, metrics in scenario_results.items()},
                    f"Dynamic Planning Safety Distribution - {scenario_name}"
                )
            )
            
            viz_file = self.track_visualization(
                self.visualizer.plot_parallel_coordinates(
                    {name: metrics for name, metrics in scenario_results.items()},
                    f"Dynamic Planning Multi-Metric Analysis - {scenario_name}"
                )
            )
            
            # Generate joint distribution plots
            for name, metrics in scenario_results.items():
                times = [m['time'] for m in metrics.values()]
                safety = [m['safety'] for m in metrics.values()]
                viz_file = self.track_visualization(
                    self.visualizer.plot_joint_distribution(
                        times, safety,
                        "Time", "Safety",
                        f"Dynamic Planning Time-Safety Distribution - {name} - {scenario_name}"
                    )
                )
            
            results[scenario_name] = scenario_results
            paths[scenario_name] = scenario_paths
            
        return results
        scenarios = [
            ('dynamic_avoidance', np.array([10, 10, 10]), np.array([180, 180, 10])),
            ('high_speed_motion', np.array([20, 180, 20]), np.array([180, 20, 20])),
            ('multi_target_dynamic', np.array([10, 10, 50]), np.array([180, 180, 50]))
        ]
        
        for scenario_name, start, goal in scenarios:
            env = Environment(size=self.config['experiment'].env_size)
            scenario_results = {}
            scenario_paths = {}
            
            for name, config in self.config['ablation'].dynamic_prediction_ablation.items():
                planner = NeuralAHPP(env)
                predictor = DynamicPredictor()
                predictor.use_lstm = config['use_lstm']
                predictor.use_uncertainty = config['use_uncertainty']
                predictor.use_attention = config['use_attention']
                planner.dynamic_predictor = predictor
                
                try:
                    path = planner.plan_path(start, goal)
                    metrics = calculate_path_metrics(path, env)
                    scenario_results[name] = metrics
                    scenario_paths[name] = path
                    
                    # Generate visualization for this configuration
                    viz_file = self.track_visualization(
                        self.visualizer.plot_3d_path_with_obstacles(
                            path, env,
                            f"Dynamic Environment Planning - {scenario_name} - {name}"
                        )
                    )
                    
                except Exception as e:
                    logger.warning(f"Failed to plan path for {name} in {scenario_name}: {e}")
                    continue
            
            results[scenario_name] = scenario_results
            paths[scenario_name] = scenario_paths
            
            # Generate comparison visualization for this scenario
            viz_file = self.track_visualization(
                self.visualizer.plot_3d_comparison(
                    scenario_paths, env,
                    f"Dynamic Environment Planning Ablation Study - {scenario_name}"
                )
            )
            
            # Generate metrics comparison
            viz_file = self.track_visualization(
                self.visualizer.plot_metrics_comparison(
                    scenario_results,
                    f"Dynamic Environment Planning Performance - {scenario_name}"
                )
            )
            
            # Generate animation
            viz_file = self.track_visualization(
                self.visualizer.create_animation(
                    scenario_paths, env,
                    f"Dynamic Environment Path Planning - {scenario_name}"
                )
            )
            
            # Generate additional visualizations
            viz_file = self.track_visualization(
                self.visualizer.plot_convergence_analysis(
                    list(range(len(scenario_results))),
                    {'safety': [r.get('safety', 0) for r in scenario_results.values()],
                     'time': [r.get('time', 0) for r in scenario_results.values()],
                     'energy': [r.get('energy', 0) for r in scenario_results.values()]},
                    f"Convergence Analysis - {scenario_name}"
                )
            )
            
            viz_file = self.track_visualization(
                self.visualizer.plot_obstacle_distribution(
                    env,
                    f"Obstacle Distribution - {scenario_name}"
                )
            )
            
            viz_file = self.track_visualization(
                self.visualizer.plot_path_characteristics(
                    scenario_paths,
                    f"Path Characteristics - {scenario_name}"
                )
            )
        
        return results
        
    def _run_dynamic_comparison(self):
        """Run dynamic environment algorithm comparison experiments"""
        env = Environment(size=self.config['experiment'].env_size)
        start = np.array([10, 10, 10])
        goal = np.array([180, 180, 10])
        results = {}
        paths = {}
        visualization_files = []
        
        # Test different algorithms
        for name, config in self.config['comparison'].dynamic_algorithms.items():
            try:
                if name == 'DWA':
                    planner = NeuralAHPP(env)
                    planner.dynamic_predictor.prediction_horizon = config['params']['prediction_time']
                elif name == 'APF':
                    planner = NeuralAHPP(env)
                    planner.repulsive_gain = config['params']['repulsive_gain']
                    planner.attractive_gain = config['params']['attractive_gain']
                else:  # MPC
                    planner = NeuralAHPP(env)
                    planner.dynamic_predictor.prediction_horizon = config['params']['horizon']
                
                path = planner.plan_path(start, goal)
                if path is not None:
                    metrics = calculate_path_metrics(path, env)
                    results[name] = metrics
                    paths[name] = path
                    
                    # Generate visualization
                    viz_file = self.track_visualization(
                        self.visualizer.plot_3d_path_with_obstacles(
                            path, env,
                            f"Dynamic Planning - {name}"
                        )
                    )
                    
            except Exception as e:
                logger.warning(f"Failed to plan path for {name}: {e}")
                continue
        
        # Generate comparison visualization
        if paths:
            viz_file = self.visualizer.plot_3d_comparison(
                paths, env,
                "Dynamic Planning Algorithm Comparison"
            )
            logger.info(f"Generated comparison visualization: {viz_file}")
            
            # Generate metrics comparison
            viz_file = self.visualizer.plot_metrics_comparison(
                results,
                "Dynamic Planning Performance Metrics"
            )
            logger.info(f"Generated metrics visualization: {viz_file}")
            
            # Generate animation
            viz_file = self.visualizer.create_animation(
                paths, env,
                "Dynamic Planning Animation"
            )
            logger.info(f"Generated animation: {viz_file}")
        
        return results
        
    def _run_dynamic_scenarios(self):
        """Run dynamic environment scenario experiments"""
        results = {}
        paths = {}
        
        # Test different scenarios
        for name, scenario in self.config['experiment'].scenarios.items():
            if 'moving_obstacles' in scenario:
                env = Environment(
                    size=self.config['experiment'].env_size,
                    num_obstacles=scenario['num_obstacles']
                )
                
                start = np.array([10, 10, 10])
                goal = np.array([180, 180, 10])
                
                try:
                    planner = NeuralAHPP(env)
                    path = planner.plan_path(start, goal)
                    
                    if path is not None:
                        metrics = calculate_path_metrics(path, env)
                        results[name] = metrics
                        paths[name] = path
                        
                        # Generate visualization
                        viz_file = self.visualizer.plot_3d_path_with_obstacles(
                            path, env,
                            f"Dynamic Scenario - {name}"
                        )
                        logger.info(f"Generated visualization: {viz_file}")
                        
                except Exception as e:
                    logger.warning(f"Failed to plan path for scenario {name}: {e}")
                    continue
        
        # Generate scenario comparison visualization
        if paths:
            viz_file = self.visualizer.plot_3d_comparison(
                paths, env,
                "Dynamic Planning Scenario Comparison"
            )
            logger.info(f"Generated comparison visualization: {viz_file}")
            
            # Generate metrics comparison
            viz_file = self.visualizer.plot_metrics_comparison(
                results,
                "Dynamic Planning Scenario Performance"
            )
            logger.info(f"Generated metrics visualization: {viz_file}")
            
            # Generate animation
            viz_file = self.visualizer.create_animation(
                paths, env,
                "Dynamic Planning Scenarios Animation"
            )
            logger.info(f"Generated animation: {viz_file}")
        
        return results
        
    def _run_cluster_ablation(self):
        """Run cluster planning ablation experiments"""
        env = Environment(size=self.config['experiment'].env_size)
        results = {}
        paths = {}
        visualization_files = []
        
        # Test different configurations
        for name, config in self.config['ablation'].cluster_planning_ablation.items():
            try:
                planner = ClusterPlanner(env, num_drones=self.config['experiment'].num_drones)
                planner.use_adaptive_clustering = config['use_adaptive_clustering']
                planner.use_attention = config['use_attention']
                planner.use_formation = config['use_formation']
                
                start_positions = [
                    np.array([10 + i*20, 10, 10]) for i in range(self.config['experiment'].num_drones)
                ]
                goal_positions = [
                    np.array([180 - i*20, 180, 10]) for i in range(self.config['experiment'].num_drones)
                ]
                
                paths_list = planner.plan_paths(start_positions, goal_positions)
                if paths_list:
                    metrics = calculate_path_metrics(np.concatenate(paths_list), env)
                    results[name] = metrics
                    paths[name] = paths_list[0]  # Show lead drone's path for visualization
                    
                    # Generate visualization
                    viz_file = self.track_visualization(
                        self.visualizer.plot_3d_path_with_obstacles(
                            paths_list[0], env,
                            f"Cluster Planning - {name}"
                        )
                    )
                    
            except Exception as e:
                logger.warning(f"Failed to plan paths for {name}: {e}")
                continue
        
        # Generate comparison visualization
        if paths:
            viz_file = self.visualizer.plot_3d_comparison(
                paths, env,
                "Cluster Planning Ablation Study"
            )
            logger.info(f"Generated comparison visualization: {viz_file}")
            
            # Generate metrics comparison
            viz_file = self.visualizer.plot_metrics_comparison(
                results,
                "Cluster Planning Performance Metrics"
            )
            logger.info(f"Generated metrics visualization: {viz_file}")
            
            # Generate animation
            viz_file = self.visualizer.create_animation(
                paths, env,
                "Cluster Planning Animation"
            )
            logger.info(f"Generated animation: {viz_file}")
        
        return results
        
    def _run_cluster_comparison(self):
        """Run cluster planning algorithm comparison experiments"""
        env = Environment(size=self.config['experiment'].env_size)
        results = {}
        paths = {}
        
        # Test different algorithms
        for name, config in self.config['comparison'].cluster_algorithms.items():
            try:
                if name == 'DMPC':
                    planner = ClusterPlanner(env, num_drones=config['params']['num_drones'])
                elif name == 'CBS':
                    planner = ClusterPlanner(env, num_drones=self.config['experiment'].num_drones)
                    planner.max_iterations = config['params']['max_iterations']
                else:  # PSO
                    planner = ClusterPlanner(env, num_drones=self.config['experiment'].num_drones)
                    planner.num_particles = config['params']['num_particles']
                    planner.iterations = config['params']['iterations']
                
                start_positions = [
                    np.array([10 + i*20, 10, 10]) for i in range(self.config['experiment'].num_drones)
                ]
                goal_positions = [
                    np.array([180 - i*20, 180, 10]) for i in range(self.config['experiment'].num_drones)
                ]
                
                paths_list = planner.plan_paths(start_positions, goal_positions)
                if paths_list:
                    metrics = calculate_path_metrics(np.concatenate(paths_list), env)
                    results[name] = metrics
                    paths[name] = paths_list[0]  # Show lead drone's path
                    
                    # Generate visualization
                    viz_file = self.track_visualization(
                        self.visualizer.plot_3d_path_with_obstacles(
                            paths_list[0], env,
                            f"Cluster Algorithm - {name}"
                        )
                    )
                    
            except Exception as e:
                logger.warning(f"Failed to plan paths for {name}: {e}")
                continue
        
        # Generate comparison visualization
        if paths:
            viz_file = self.track_visualization(
                self.visualizer.plot_3d_comparison(
                    paths, env,
                    "Cluster Algorithm Comparison"
                )
            )
            
            # Generate metrics comparison
            viz_file = self.track_visualization(
                self.visualizer.plot_metrics_comparison(
                    results,
                    "Cluster Algorithm Performance"
                )
            )
            
            # Generate animation
            viz_file = self.track_visualization(
                self.visualizer.create_animation(
                    paths, env,
                    "Cluster Algorithm Animation"
                )
            )
        
        return results
        
    def _run_cluster_scenarios(self):
        """Run cluster planning scenario experiments"""
        results = {}
        paths = {}
        
        # Test different scenarios
        for name, scenario in self.config['experiment'].scenarios.items():
            env = Environment(
                size=self.config['experiment'].env_size,
                num_obstacles=scenario['num_obstacles']
            )
            
            try:
                planner = ClusterPlanner(env, num_drones=self.config['experiment'].num_drones)
                
                start_positions = [
                    np.array([10 + i*20, 10, 10]) for i in range(self.config['experiment'].num_drones)
                ]
                goal_positions = [
                    np.array([180 - i*20, 180, 10]) for i in range(self.config['experiment'].num_drones)
                ]
                
                paths_list = planner.plan_paths(start_positions, goal_positions)
                if paths_list:
                    metrics = calculate_path_metrics(np.concatenate(paths_list), env)
                    results[name] = metrics
                    paths[name] = paths_list[0]  # Show lead drone's path
                    
                    # Generate visualization
                    viz_file = self.track_visualization(
                        self.visualizer.plot_3d_path_with_obstacles(
                            paths_list[0], env,
                            f"Cluster Scenario - {name}"
                        )
                    )
                    
            except Exception as e:
                logger.warning(f"Failed to plan paths for scenario {name}: {e}")
                continue
        
        # Generate scenario comparison visualization
        if paths:
            viz_file = self.track_visualization(
                self.visualizer.plot_3d_comparison(
                    paths, env,
                    "Cluster Planning Scenario Comparison"
                )
            )
            
            # Generate metrics comparison
            viz_file = self.track_visualization(
                self.visualizer.plot_metrics_comparison(
                    results,
                    "Cluster Planning Scenario Performance"
                )
            )
            
            # Generate animation
            viz_file = self.track_visualization(
                self.visualizer.create_animation(
                    paths, env,
                    "Cluster Planning Scenarios Animation"
                )
            )
            
            # Generate additional visualizations
            viz_file = self.track_visualization(
                self.visualizer.plot_convergence_analysis(
                    list(range(len(results))),
                    {'safety': [r.get('safety', 0) for r in results.values()],
                     'time': [r.get('time', 0) for r in results.values()],
                     'energy': [r.get('energy', 0) for r in results.values()]},
                    f"Cluster Planning Convergence Analysis"
                )
            )
            
            viz_file = self.track_visualization(
                self.visualizer.plot_obstacle_distribution(
                    env,
                    f"Cluster Planning Obstacle Distribution"
                )
            )
            
            viz_file = self.track_visualization(
                self.visualizer.plot_path_characteristics(
                    paths,
                    f"Cluster Planning Path Characteristics"
                )
            )
        
        return results
        
    def generate_visualizations(self, neural_results, dynamic_results, cluster_results):
        """Generate all visualizations with tracking"""
        visualization_files = []
        
        # 1. Neural Evolution Algorithm Visualizations
        viz_file = self.track_visualization(
            self.visualizer.plot_ablation_study(
                neural_results['ablation'],
                "Neural Evolution Ablation Study"
            )
        )
        
        viz_file = self.track_visualization(
            self.visualizer.plot_metrics_comparison(
                neural_results['comparison'],
                "Neural Evolution Performance Comparison"
            )
        )
        
        viz_file = self.track_visualization(
            self.visualizer.plot_scenario_comparison(
                {'neural': neural_results['scenarios']},
                "Neural Evolution Scenario Results"
            )
        )
        
        # 2. Dynamic Environment Visualizations
        viz_file = self.track_visualization(
            self.visualizer.plot_ablation_study(
                dynamic_results['ablation'],
                "Dynamic Environment Ablation Study"
            )
        )
        
        viz_file = self.track_visualization(
            self.visualizer.plot_metrics_comparison(
                dynamic_results['comparison'],
                "Dynamic Environment Performance Comparison"
            )
        )
        
        viz_file = self.track_visualization(
            self.visualizer.plot_scenario_comparison(
                {'dynamic': dynamic_results['scenarios']},
                "Dynamic Environment Scenario Results"
            )
        )
        
        # 3. Cluster Planning Visualizations
        viz_file = self.track_visualization(
            self.visualizer.plot_ablation_study(
                cluster_results['ablation'],
                "Cluster Planning Ablation Study"
            )
        )
        
        viz_file = self.track_visualization(
            self.visualizer.plot_metrics_comparison(
                cluster_results['comparison'],
                "Cluster Planning Performance Comparison"
            )
        )
        
        viz_file = self.track_visualization(
            self.visualizer.plot_scenario_comparison(
                {'cluster': cluster_results['scenarios']},
                "Cluster Planning Scenario Results"
            )
        )
        
        # 4. Cross-Chapter Performance Analysis
        combined_scenarios = {
            'neural': neural_results['scenarios'],
            'dynamic': dynamic_results['scenarios'],
            'cluster': cluster_results['scenarios']
        }
        viz_file = self.track_visualization(
            self.visualizer.plot_scenario_comparison(
                combined_scenarios,
                "Cross-Chapter Performance Analysis"
            )
        )
        
        # 5. Generate heatmaps for path density analysis
        for chapter, results in [
            ('Neural', neural_results),
            ('Dynamic', dynamic_results),
            ('Cluster', cluster_results)
        ]:
            viz_file = self.track_visualization(
                self.visualizer.plot_heatmap(
                    results['scenarios'],
                    f"{chapter} Path Density Analysis"
                )
            )
            
            # Additional visualizations per chapter
            viz_file = self.track_visualization(
                self.visualizer.plot_convergence_analysis(
                    list(range(len(results['ablation']))),
                    {'safety': [r.get('safety', 0) for r in results['ablation'].values()],
                     'time': [r.get('time', 0) for r in results['ablation'].values()],
                     'energy': [r.get('energy', 0) for r in results['ablation'].values()]},
                    f"{chapter} Convergence Analysis"
                )
            )
            
            viz_file = self.track_visualization(
                self.visualizer.plot_obstacle_distribution(
                    Environment(size=[200, 200, 100], num_obstacles=20),
                    f"{chapter} Obstacle Distribution"
                )
            )
            
            viz_file = self.track_visualization(
                self.visualizer.plot_path_characteristics(
                    results['comparison'],
                    f"{chapter} Path Characteristics"
                )
            )
        
        # Report visualization count
        valid_files = [f for f in visualization_files if f]
        logger.info(f"\nGenerated {len(valid_files)} visualizations:")
        for i, viz_file in enumerate(valid_files, 1):
            logger.info(f"{i}. {viz_file}")
        
        return visualization_files

if __name__ == "__main__":
    runner = ExperimentRunner()
    results = runner.run_all_experiments()
    
    logger.info("\nExperiments completed! Generated the following visualizations:")
    for viz_file in results['visualizations']:
        logger.info(f"- {viz_file}")
