# 第四章：动态环境下的UAV路径规划算法

## 代码结构
- `algorithms/dynamic_predictor.py`: LSTM预测器实现
- `algorithms/uav_dppa_dwa.py`: 动态窗口方法实现
- `utils_new.py`: 动态环境相关工具函数

## 核心创新点
1. LSTM动态预测：准确预测障碍物运动轨迹
2. 不确定性估计：提高规划决策的鲁棒性
3. 自适应动态窗口：优化局部路径规划

## 实验结果
### 1. 性能指标对比
- 预测准确率
- 实时性能
- 避障成功率
- 路径平滑度
相关可视化：`results/动态环境规划性能指标对比_*.png`

### 2. 消融实验
对比了以下模块的贡献：
- 基础模型
- LSTM预测
- 不确定性估计
- 完整模型
相关可视化：`results/动态环境规划消融实验对比_*.png`

### 3. 场景测试
在三种动态场景下进行测试：
- 动态避障场景
- 高速运动场景
- 多目标动态场景
相关可视化：
- `results/动态环境规划_-_动态避障场景_*.png`
- `results/动态环境规划_-_高速运动场景_*.png`
- `results/动态环境规划_-_多目标动态_*.png`

### 4. 动态可视化
算法执行过程的动态展示：
- `results/动态环境规划路径动画_*.gif`
- `results/动态环境规划路径动画_*_path_sequence.png`

## 参考文献
1. LSTM: Long Short-Term Memory (Hochreiter & Schmidhuber, 1997)
2. Dynamic Window Approach to Collision Avoidance (Fox et al., 1997)
3. Uncertainty-Aware Reinforcement Learning for Collision Avoidance (Kahn et al., 2017)
