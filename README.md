# UAV路径规划算法改进与实现

本项目实现了三种创新的UAV路径规划算法，包括基于神经进化的路径规划、动态环境下的路径规划和基于集群智能的路径规划。

## 项目结构

```
PathPlan/
├── algorithms/           # 算法实现
│   ├── neural_ahpp.py           # 神经进化算法
│   ├── dynamic_predictor.py     # 动态预测器
│   ├── cluster_planner.py       # 集群规划算法
│   └── rrt_star.py             # RRT*算法
├── experiments/         # 实验代码
│   ├── run_experiments.py       # 实验运行脚本
│   ├── visualization_enhanced.py # 可视化生成
│   └── config.py               # 实验配置
├── results/            # 实验结果
│   ├── *.png                    # 静态图表
│   └── *.gif                    # 动态可视化
├── chapter3_neural_evolution.md  # 第三章详细说明
├── chapter4_dynamic_planning.md  # 第四章详细说明
└── chapter5_cluster_planning.md  # 第五章详细说明
```

## 主要创新点

1. 第三章：基于神经进化的路径规划
   - 注意力机制增强
   - 经验回放优化
   - 自适应进化策略

2. 第四章：动态环境下的路径规划
   - LSTM动态预测
   - 不确定性估计
   - 自适应动态窗口

3. 第五章：基于集群智能的路径规划
   - 自适应集群形成
   - 分布式决策机制
   - 多目标优化

## 实验结果

总共生成了54+个可视化结果，包括：
- 性能指标对比图
- 消融实验分析
- 场景测试结果
- 动态规划过程

详细结果请参考各章节的说明文档和results目录。

## 运行说明

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行实验：
```bash
python experiments/run_experiments.py
```

3. 生成可视化：
```bash
python experiments/visualization_enhanced.py
```

## 参考文献

详见各章节说明文档中的参考文献部分。
