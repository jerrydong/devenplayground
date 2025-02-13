import matplotlib.pyplot as plt
import logging
from experiments.visualization_enhanced_v2 import EnhancedVisualizerV2
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_chinese_rendering():
    """Test Chinese character rendering with comprehensive text"""
    viz = EnhancedVisualizerV2()
    
    # Create test figure with comprehensive Chinese text
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Title and labels
    fig.suptitle("无人机路径规划算法性能分析", fontsize=16)
    
    # Plot 1: Path length comparison
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    ax1.plot(x, y1)
    ax1.set_title("路径长度对比")
    ax1.set_xlabel("迭代次数")
    ax1.set_ylabel("路径长度 (米)")
    
    # Plot 2: Smoothness analysis
    y2 = np.cos(x)
    ax2.plot(x, y2)
    ax2.set_title("平滑度分析")
    ax2.set_xlabel("路径点")
    ax2.set_ylabel("曲率")
    
    # Plot 3: Obstacle avoidance
    y3 = x**2/100
    ax3.plot(x, y3)
    ax3.set_title("避障性能")
    ax3.set_xlabel("障碍物数量")
    ax3.set_ylabel("成功率 (%)")
    
    # Plot 4: Computation time
    y4 = np.log(x+1)
    ax4.plot(x, y4)
    ax4.set_title("计算时间")
    ax4.set_xlabel("环境复杂度")
    ax4.set_ylabel("时间 (秒)")
    
    plt.tight_layout()
    
    # Save with Chinese characters
    filename = "chinese_font_comprehensive_test.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    # Move to organized directory using visualizer
    viz.save_visualization(filename, chapter=3, category='performance', subcategory='analysis')
    logger.info("Comprehensive Chinese font test completed")

if __name__ == "__main__":
    test_chinese_rendering()
