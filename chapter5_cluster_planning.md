# 第五章：基于集群智能的UAV路径规划算法

## 代码结构
- `algorithms/cluster_planner.py`: 基础集群规划算法
- `algorithms/cluster_planner_new.py`: 改进的集群规划算法
- `algorithms/rrt_star.py`: RRT*算法实现

## 核心创新点
1. 自适应集群形成：动态调整集群结构
2. 分布式决策机制：提高系统可扩展性
3. 多目标优化：平衡路径长度、能量消耗和任务完成时间

## 实验结果
### 1. 性能指标对比
- 集群协同效率
- 计算开销
- 任务完成率
- 能量效率
相关可视化：`results/cluster_formation.png`

### 2. 消融实验
对比了以下模块的贡献：
- 基础RRT*
- 自适应集群
- 分布式决策
- 完整模型
相关可视化：
- `results/Neural_Evolution_Ablation_Study_*.png`
- `results/Dynamic_Planning_Performance_Metrics.png`

### 3. 场景测试
在不同规模和复杂度的场景下测试：
- 小规模集群（5架无人机）
- 中规模集群（10架无人机）
- 大规模集群（20架无人机）
相关可视化：
- `results/Dynamic_Planning_-_*.png`
- `results/Neural_Evolution_Path_Planning_*.png`

### 4. 动态可视化
集群协同过程的动态展示：
- `results/path_planning_animation.gif`
- `results/Dynamic_Planning_Animation_path_sequence.png`

## 参考文献
1. RRT*: Optimal and efficient path planning for unknown environments (Karaman & Frazzoli, 2011)
2. Distributed Multi-Robot Formation Control among Obstacles (Alonso-Mora et al., 2017)
3. Energy-Aware Path Planning for UAV Swarms (Zhang et al., 2019)
