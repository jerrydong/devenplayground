import os
import shutil
import re

def get_chapter_and_category(filename):
    """Determine chapter and category from filename"""
    chapter = 3  # Default chapter
    
    # Chapter detection
    if "neural" in filename.lower() or "evolution" in filename.lower():
        chapter = 3
    elif "dynamic" in filename.lower() or "predictor" in filename.lower():
        chapter = 4
    elif "cluster" in filename.lower() or "swarm" in filename.lower():
        chapter = 5
        
    # Category detection
    if any(x in filename.lower() for x in ["metric", "performance", "comparison", "analysis"]):
        category = "performance"
        subcategory = "metrics" if "metric" in filename.lower() else "analysis"
    elif "ablation" in filename.lower():
        category = "ablation"
        subcategory = "components"
    elif any(x in filename.lower() for x in ["scenario", "test", "environment"]):
        category = "scenarios"
        subcategory = "simple"
    elif any(x in filename.lower() for x in ["animation", "sequence", "dynamic"]):
        category = "animations"
        subcategory = "paths"
    else:
        category = "performance"
        subcategory = "analysis"
        
    return chapter, category, subcategory

def organize_visualizations():
    """Organize visualization files into proper directory structure"""
    base_dir = "organized_results"
    
    # Get all PNG files
    png_files = [f for f in os.listdir(".") if f.endswith(".png")]
    
    for filename in png_files:
        chapter, category, subcategory = get_chapter_and_category(filename)
        
        # Create target directory
        target_dir = os.path.join(base_dir, f"chapter{chapter}", category, subcategory)
        os.makedirs(target_dir, exist_ok=True)
        
        # Move file
        target_path = os.path.join(target_dir, filename)
        try:
            shutil.move(filename, target_path)
            print(f"Moved {filename} to {target_path}")
        except Exception as e:
            print(f"Failed to move {filename}: {e}")

if __name__ == "__main__":
    organize_visualizations()
