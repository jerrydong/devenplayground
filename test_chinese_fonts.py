import matplotlib.pyplot as plt
import logging
from experiments.visualization_enhanced_v2 import EnhancedVisualizerV2
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_chinese_rendering():
    """Test Chinese character rendering in visualizations"""
    viz = EnhancedVisualizerV2()
    
    # Create test figure with Chinese characters
    fig = plt.figure(figsize=(10, 6))
    plt.title("中文字体测试")
    plt.xlabel("路径长度 (米)")
    plt.ylabel("平滑度得分")
    
    # Add some sample data
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plt.plot(x, y, label="测试曲线")
    plt.legend()
    
    # Save with Chinese characters
    filename = "chinese_font_test.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    # Move to organized directory using visualizer
    viz.save_visualization(filename, chapter=3, category='performance', subcategory='analysis')
    logger.info("Chinese font test completed")

if __name__ == "__main__":
    test_chinese_rendering()
