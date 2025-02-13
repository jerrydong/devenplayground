import os
import shutil
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def rename_visualizations():
    """Rename visualization files to follow convention"""
    base_dir = "organized_results"
    
    # Mapping of old names to new standardized names with proper categories
    rename_map = {
        'test_results.png': 'ch3_scenarios_simple_path_test.png',
        'chinese_font_comprehensive_test.png': 'ch3_performance_analysis_font_comprehensive.png',
        'chinese_font_test.png': 'ch3_performance_analysis_font_basic.png',
        'composite_path_planning_results.png': 'ch3_performance_metrics_composite.png',
        'path_planning_results_1.png': 'ch3_performance_metrics_results_1.png',
        'path_planning_results_2.png': 'ch3_performance_metrics_results_2.png',
        'path_planning_results_3.png': 'ch3_performance_metrics_results_3.png',
        'ch3_performance_analysis_RRT_Path_Smoothness_Test.png': 'ch3_performance_analysis_smoothness.png',
        'ch3_performance_analysis_Path_Planning_Smoothness_Comparison.png': 'ch3_performance_comparison_smoothness.png'
    }
    
    # Walk through directory structure
    for root, dirs, files in os.walk(base_dir):
        for old_name in files:
            if old_name in rename_map:
                old_path = os.path.join(root, old_name)
                new_name = rename_map[old_name]
                
                # Determine correct directory based on new name
                parts = new_name.split('_')
                chapter = parts[0]  # ch3
                category = parts[1]  # performance/scenarios
                subcategory = parts[2]  # analysis/simple
                
                new_dir = os.path.join(base_dir, f"{chapter.replace('ch', 'chapter')}", 
                                     category, subcategory)
                os.makedirs(new_dir, exist_ok=True)
                
                new_path = os.path.join(new_dir, new_name)
                
                try:
                    shutil.move(old_path, new_path)
                    logger.info(f"Renamed: {old_name} -> {new_name}")
                except Exception as e:
                    logger.error(f"Failed to rename {old_name}: {e}")

if __name__ == "__main__":
    rename_visualizations()
