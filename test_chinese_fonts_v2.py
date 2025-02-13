import matplotlib.pyplot as plt
import matplotlib as mpl
import logging
import os
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_chinese_fonts():
    """Test Chinese font rendering with comprehensive test cases"""
    # Set locale environment
    os.environ['LANG'] = 'zh_CN.UTF-8'
    os.environ['LC_ALL'] = 'zh_CN.UTF-8'
    
    # Primary font list with fallbacks
    chinese_fonts = [
        'WenQuanYi Micro Hei',  # Most widely available
        'Noto Sans CJK SC',     # Google's font, good coverage
        'AR PL UMing CN',       # Traditional Chinese
        'AR PL KaitiM GB',      # Simplified Chinese
        'WenQuanYi Zen Hei',    # Another WenQuanYi font
        'SimHei',               # Common Chinese font
        'Microsoft YaHei',      # Windows font
        'Noto Sans CJK TC',     # Traditional Chinese fallback
        'DejaVu Sans'           # Default fallback
    ]
    
    # Configure font settings
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': chinese_fonts,
        'axes.unicode_minus': False,
        'font.size': 12,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'text.usetex': False,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.1,
        'figure.autolayout': True,
        'mathtext.fontset': 'custom',
        'mathtext.rm': 'WenQuanYi Micro Hei',
        'mathtext.it': 'WenQuanYi Micro Hei',
        'mathtext.bf': 'WenQuanYi Micro Hei'
    })
    
    # Test strings
    test_strings = [
        "基本测试文本",
        "复杂的中文字符测试：你好，世界！",
        "数学公式：α = β + γ",
        "混合文本 ABC 123 测试",
        "标题文字大小测试",
        "图例和标签测试",
        "网格线和刻度标签",
        "多行\n文本\n测试"
    ]
    
    # Create test figure
    fig = plt.figure(figsize=(15, 10))
    
    # Test different text elements
    for i, test_str in enumerate(test_strings):
        plt.subplot(2, 4, i+1)
        plt.plot([0, 1], [0, 1], label=test_str)
        plt.title(f"测试 {i+1}")
        plt.xlabel("X轴")
        plt.ylabel("Y轴")
        plt.legend()
        plt.grid(True)
    
    plt.suptitle("中文字体渲染测试", fontsize=16)
    
    # Save test figure
    output_dir = "test_results"
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, "chinese_font_test.png"))
    plt.close()
    
    # Test each font individually
    fig, axes = plt.subplots(3, 3, figsize=(15, 15))
    test_str = "中文字体测试 ABC 123"
    
    for i, font in enumerate(chinese_fonts):
        row = i // 3
        col = i % 3
        ax = axes[row, col]
        
        try:
            ax.text(0.5, 0.5, test_str, fontsize=12, family=font,
                   ha='center', va='center')
            ax.set_title(f"Font: {font}")
            logger.info(f"Successfully tested font: {font}")
        except Exception as e:
            logger.warning(f"Failed to test font {font}: {e}")
        
        ax.set_xticks([])
        ax.set_yticks([])
    
    plt.suptitle("各字体渲染效果对比", fontsize=16)
    plt.savefig(os.path.join(output_dir, "font_comparison.png"))
    plt.close()
    
    logger.info("Completed Chinese font rendering tests")

if __name__ == "__main__":
    test_chinese_fonts()
