"""Visualization utilities for experiment results analysis."""

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
import numpy as np
import json
from pathlib import Path
import pandas as pd

class ExperimentVisualizer:
    def __init__(self):
        self.results_dir = Path('results')
        self.figures_dir = self.results_dir / 'figures'
        self.figures_dir.mkdir(parents=True, exist_ok=True)
        
        # Use default style with improved aesthetics
        plt.rcParams['figure.figsize'] = [12, 8]
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3
        plt.rcParams['axes.facecolor'] = '#f0f0f0'
        plt.rcParams['figure.facecolor'] = 'white'
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['axes.titlesize'] = 14
        
    def plot_ablation_results(self):
        """Plot ablation study results with grouped metrics."""
        with open(self.results_dir / 'ablation/ablation_results.json', 'r') as f:
            results = json.load(f)
            
        # Create figure with multiple subplots
        fig = plt.figure(figsize=(20, 15))
        gs = GridSpec(3, 2)
        
        # 1. Standard Metrics
        ax1 = fig.add_subplot(gs[0, 0])
        metrics = ['accuracy', 'precision', 'recall', 'f1_score']
        variants = list(results.keys())
        x = np.arange(len(variants))
        width = 0.2
        
        for i, metric in enumerate(metrics):
            values = [results[v]['standard_metrics'][metric] for v in variants]
            ax1.bar(x + i*width, values, width, label=metric.capitalize())
            
        ax1.set_xlabel('Model Variants')
        ax1.set_ylabel('Score')
        ax1.set_title('Standard Metrics')
        ax1.set_xticks(x + width*1.5)
        ax1.set_xticklabels(variants, rotation=45)
        ax1.legend()
        
        # 2. Feature Enhancement Metrics
        ax2 = fig.add_subplot(gs[0, 1])
        metrics = ['denoising_effectiveness', 'multi_view_consistency', 'feature_pyramid_quality']
        for i, metric in enumerate(metrics):
            values = [results[v]['feature_enhancement'][metric] for v in variants]
            ax2.bar(x + i*width, values, width, label=metric.replace('_', ' ').title())
        ax2.set_title('Feature Enhancement Metrics')
        ax2.set_xticks(x + width*1.5)
        ax2.set_xticklabels(variants, rotation=45)
        ax2.legend()
        
        # 3. Domain Adaptation Metrics
        ax3 = fig.add_subplot(gs[1, :])
        metrics = ['domain_alignment_score', 'feature_similarity', 'transfer_gap']
        for i, metric in enumerate(metrics):
            values = [results[v]['domain_adaptation'][metric] for v in variants]
            ax3.bar(x + i*width, values, width, label=metric.replace('_', ' ').title())
        ax3.set_title('Domain Adaptation Metrics')
        ax3.set_xticks(x + width*1.5)
        ax3.set_xticklabels(variants, rotation=45)
        ax3.legend()
        
        plt.tight_layout()
        plt.savefig(self.figures_dir / 'ablation_results.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def plot_comparative_results(self):
        """Plot comparative study results."""
        with open(self.results_dir / 'comparative/comparative_results.json', 'r') as f:
            results = json.load(f)
            
        scenarios = list(results.keys())
        models = list(results[scenarios[0]].keys())
        metrics = ['accuracy', 'precision', 'recall', 'f1_score']
        
        # Create figure for each scenario
        for scenario in scenarios:
            fig = plt.figure(figsize=(15, 10))
            gs = GridSpec(2, 2)
            
            # Plot each metric
            for i, metric in enumerate(metrics):
                ax = fig.add_subplot(gs[i//2, i%2])
                values = [results[scenario][model]['standard_metrics'][metric] for model in models]
                sns.barplot(x=models, y=values, ax=ax)
                ax.set_title(f'{metric.capitalize()} - {scenario}')
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
                
            plt.tight_layout()
            plt.savefig(self.figures_dir / f'comparative_results_{scenario}.png', dpi=300, bbox_inches='tight')
            plt.close()
            
    def plot_domain_adaptation_analysis(self):
        """Plot domain adaptation performance analysis."""
        with open(self.results_dir / 'ablation/ablation_results.json', 'r') as f:
            results = json.load(f)
            
        fig = plt.figure(figsize=(15, 10))
        gs = GridSpec(2, 2)
        
        # 1. Domain Alignment Score
        ax1 = fig.add_subplot(gs[0, 0])
        variants = list(results.keys())
        scores = [results[v]['domain_adaptation']['domain_alignment_score'] for v in variants]
        sns.barplot(x=variants, y=scores, ax=ax1)
        ax1.set_title('Domain Alignment Score')
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
        
        # 2. Feature Similarity vs Transfer Gap
        ax2 = fig.add_subplot(gs[0, 1])
        similarity = [results[v]['domain_adaptation']['feature_similarity'] for v in variants]
        transfer_gap = [results[v]['domain_adaptation']['transfer_gap'] for v in variants]
        ax2.scatter(similarity, transfer_gap)
        for i, txt in enumerate(variants):
            ax2.annotate(txt, (similarity[i], transfer_gap[i]))
        ax2.set_xlabel('Feature Similarity')
        ax2.set_ylabel('Transfer Gap')
        ax2.set_title('Feature Similarity vs Transfer Gap')
        
        plt.tight_layout()
        plt.savefig(self.figures_dir / 'domain_adaptation_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def plot_computational_efficiency(self):
        """Plot computational efficiency metrics."""
        with open(self.results_dir / 'comparative/comparative_results.json', 'r') as f:
            results = json.load(f)
            
        # Extract computational metrics
        models = list(results[list(results.keys())[0]].keys())
        metrics = ['inference_time', 'memory_usage', 'model_size']
        
        fig = plt.figure(figsize=(15, 5))
        gs = GridSpec(1, 3)
        
        for i, metric in enumerate(metrics):
            ax = fig.add_subplot(gs[0, i])
            values = [results[list(results.keys())[0]][model]['computational'][metric] 
                     for model in models]
            sns.barplot(x=models, y=values, ax=ax)
            ax.set_title(f'{metric.replace("_", " ").title()}')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            
        plt.tight_layout()
        plt.savefig(self.figures_dir / 'computational_efficiency.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def plot_scenario_performance(self):
        """Plot scenario-specific performance analysis."""
        with open(self.results_dir / 'ablation/ablation_results.json', 'r') as f:
            results = json.load(f)
            
        fig = plt.figure(figsize=(15, 10))
        gs = GridSpec(2, 2)
        
        # 1. Through-wall Performance
        ax1 = fig.add_subplot(gs[0, 0])
        variants = list(results.keys())
        accuracy = [results[v]['scenario_specific']['through_wall_accuracy'] for v in variants]
        sns.barplot(x=variants, y=accuracy, ax=ax1)
        ax1.set_title('Through-wall Recognition Accuracy')
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
        
        # 2. Multi-person Detection
        ax2 = fig.add_subplot(gs[0, 1])
        detection = [results[v]['scenario_specific']['multi_person_detection_rate'] for v in variants]
        sns.barplot(x=variants, y=detection, ax=ax2)
        ax2.set_title('Multi-person Detection Rate')
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
        
        # 3. Environmental Stability
        ax3 = fig.add_subplot(gs[1, :])
        stability = [results[v]['scenario_specific']['environmental_stability'] for v in variants]
        sns.barplot(x=variants, y=stability, ax=ax3)
        ax3.set_title('Environmental Stability')
        ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45)
        
        plt.tight_layout()
        plt.savefig(self.figures_dir / 'scenario_performance.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def visualize_all_results(self):
        """Generate all visualizations."""
        print("Generating ablation study visualizations...")
        self.plot_ablation_results()
        
        print("Generating comparative study visualizations...")
        self.plot_comparative_results()
        
        print("Generating domain adaptation analysis...")
        self.plot_domain_adaptation_analysis()
        
        print("Generating computational efficiency analysis...")
        self.plot_computational_efficiency()
        
        print("Generating scenario-specific performance analysis...")
        self.plot_scenario_performance()
        
        print(f"All visualizations saved to {self.figures_dir}")

if __name__ == '__main__':
    visualizer = ExperimentVisualizer()
    visualizer.visualize_all_results()
