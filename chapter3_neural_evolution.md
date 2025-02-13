# 第三章：基于神经进化的UAV路径规划算法

## 代码结构
- `algorithms/neural_ahpp.py`: 基础神经进化算法实现
- `algorithms/neural_ahpp_improved.py`: 改进的神经进化算法，添加了注意力机制
- `algorithms/neural_ahpp_final.py`: 最终版本，集成了经验回放等优化

## 核心创新点
1. 注意力机制增强：优化对障碍物和目标点的感知
2. 经验回放优化：提高训练效率和收敛性能
3. 自适应进化策略：动态调整变异和交叉概率

## 实验结果
### 1. 性能指标对比
- 路径长度
- 计算时间
- 避障成功率
- 路径平滑度
相关可视化：`results/神经进化算法性能指标对比_*.png`

### 2. 消融实验
对比了以下模块的贡献：
- 基础模型
- 注意力机制
- 经验回放
- 完整模型
相关可视化：`results/神经进化算法消融实验对比_*.png`

### 3. 场景测试
在三种典型场景下进行测试：
- 简单场景
- 复杂场景
- 狭窄场景
相关可视化：
- `results/神经进化算法_-_简单场景_*.png`
- `results/神经进化算法_-_复杂场景_*.png`
- `results/神经进化算法_-_狭窄场景_*.png`

### 4. 动态可视化
算法执行过程的动态展示：
- `results/神经进化算法路径规划动画_*.gif`
- `results/神经进化算法路径规划动画_*_path_sequence.png`

## 参考文献
1. Attention Is All You Need (Vaswani et al., 2017)
2. Deep Neuroevolution: Genetic Algorithms Are a Competitive Alternative for Training Deep Neural Networks for Reinforcement Learning (Such et al., 2018)
3. Evolution Strategies as a Scalable Alternative to Reinforcement Learning (Salimans et al., 2017)
