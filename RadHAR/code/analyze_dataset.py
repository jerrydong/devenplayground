import os
import numpy as np
import yaml

def analyze_data_file(file_path):
    """分析单个数据文件的维度和样本信息"""
    points = []
    current_point = {}
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if line == '---':
            if current_point:
                points.append(current_point)
                current_point = {}
        elif ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            if value:  # 如果值不为空
                try:
                    value = float(value)
                    current_point[key] = value
                except ValueError:
                    pass
    
    # 提取特征维度
    if points:
        features = list(points[0].keys())
        features = [f for f in features if isinstance(points[0][f], (int, float))]
        return len(points), len(features), features
    return 0, 0, []

def analyze_dataset():
    """分析整个数据集的信息"""
    base_path = "../data/Data/Train"
    
    # 获取所有动作类型
    action_types = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    
    print("\n=== RadHAR数据集分析 ===")
    print(f"\n1. 动作类型数量: {len(action_types)}")
    print(f"动作类型列表: {sorted(action_types)}")
    
    # 分析每种动作的样本数量
    total_samples = 0
    samples_per_action = {}
    
    # 记录维度信息
    dimensions = None
    features = None
    
    print("\n2. 每种动作的样本数量:")
    for action in sorted(action_types):
        action_path = os.path.join(base_path, action)
        samples = [f for f in os.listdir(action_path) if f.endswith('.txt')]
        samples_per_action[action] = len(samples)
        total_samples += len(samples)
        
        # 分析第一个样本的维度
        if not dimensions:
            first_sample = os.path.join(action_path, samples[0])
            num_points, num_features, feature_list = analyze_data_file(first_sample)
            dimensions = num_features
            features = feature_list
        
        print(f"   - {action}: {len(samples)}个样本")
    
    print(f"\n3. 总样本数量: {total_samples}")
    
    print(f"\n4. 数据维度信息:")
    print(f"   - 特征维度: {dimensions}")
    print(f"   - 特征列表: {features}")
    
    # 计算平均每个样本的点数
    total_points = 0
    num_files = 0
    for action in action_types:
        action_path = os.path.join(base_path, action)
        for sample in os.listdir(action_path):
            if sample.endswith('.txt'):
                file_path = os.path.join(action_path, sample)
                points, _, _ = analyze_data_file(file_path)
                total_points += points
                num_files += 1
    
    avg_points = total_points / num_files if num_files > 0 else 0
    print(f"\n5. 样本大小信息:")
    print(f"   - 平均每个样本包含的点数: {avg_points:.2f}")
    print(f"   - 所有样本的总点数: {total_points}")

if __name__ == "__main__":
    analyze_dataset()
