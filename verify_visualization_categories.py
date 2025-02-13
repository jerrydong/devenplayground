import os
import re
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_visualization_categories():
    """Verify visualization categorization and naming convention"""
    base_dir = "organized_results"
    
    # Expected categories and subcategories
    expected_categories = {
        'performance': ['metrics', 'comparison', 'analysis'],
        'ablation': ['components', 'experiments', 'results'],
        'scenarios': ['simple', 'complex', 'dynamic'],
        'animations': ['paths', 'sequences', 'interactive']
    }
    
    # Track statistics
    stats = {
        'chapter3': {'total': 0, 'categories': {}},
        'chapter4': {'total': 0, 'categories': {}},
        'chapter5': {'total': 0, 'categories': {}}
    }
    
    # Filename pattern - match category and subcategory
    pattern = re.compile(r'^ch(\d)_(performance|ablation|scenarios|animations)_(metrics|comparison|analysis|components|experiments|results|simple|complex|dynamic|paths|sequences|interactive)_.*\.png$')
    
    # Walk through directory structure
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.png'):
                # Get relative path
                rel_path = os.path.relpath(root, base_dir)
                chapter_dir = rel_path.split(os.sep)[0]
                
                if chapter_dir.startswith('chapter'):
                    # Update statistics
                    stats[chapter_dir]['total'] += 1
                    
                    # Check filename format
                    match = pattern.match(file)
                    if not match:
                        logger.warning(f"File does not follow naming convention: {file}")
                        continue
                    
                    chapter, category, subcategory = match.groups()
                    
                    # Update category statistics
                    if category not in stats[chapter_dir]['categories']:
                        stats[chapter_dir]['categories'][category] = 0
                    stats[chapter_dir]['categories'][category] += 1
                    
                    # Verify category and subcategory
                    if category not in expected_categories:
                        logger.warning(f"Unexpected category '{category}' in file: {file}")
                    elif subcategory not in expected_categories[category]:
                        logger.warning(f"Unexpected subcategory '{subcategory}' for category '{category}' in file: {file}")
    
    # Report statistics
    logger.info("\nVisualization Statistics:")
    for chapter, data in stats.items():
        logger.info(f"\n{chapter}:")
        logger.info(f"Total visualizations: {data['total']}")
        logger.info("Category breakdown:")
        for category, count in data['categories'].items():
            logger.info(f"  {category}: {count}")
        
        # Check for missing categories
        missing = set(expected_categories.keys()) - set(data['categories'].keys())
        if missing:
            logger.warning(f"Missing categories in {chapter}: {missing}")

if __name__ == "__main__":
    verify_visualization_categories()
