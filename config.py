import numpy as np

# 环境配置
ENV_SIZE = (300.0, 300.0, 300.0)  # 环境大小 (长, 宽, 高)
# ENV_SIZE = (1000.0, 1000.0, 1000.0)  # 环境大小 (长, 宽, 高)
NUM_OBSTACLES = 30                # 障碍物数量
OBSTACLE_DISTRIBUTION = {
    'dispersion_factor': 3.0,     # 分散度系数，值越大障碍物越分散
    'overlap_tolerance': 'none',   # 重叠容忍度：'normal', 'low', 'none'
}
OBSTACLE_SHAPE = 'cuboid'  # 默认障碍物形状为立方体，可选值：长方体-'cuboid', 椭圆-'ellipsoid', 圆柱-'cylinder', 正方体-'cube'
OBSTACLE_OPACITY = False           # 障碍物是否透明，True 表示透明，False 表示不透明
# 【配置】设置障碍物颜色，默认为黑色，可以是 matplotlib 支持的颜色字符串、十六进制颜色代码或 RGB 元组。
OBSTACLE_COLOR = '#000000'  # 障碍物颜色配置项

# 无人机参数配置
DRONE_MAX_SPEED = 10.0            # 最大飞行速度 (单位：米/秒)
DRONE_MIN_TURN_RADIUS = 10.0      # 最小转弯半径 (单位：米)
DRONE_PERCEPTION_RANGE = 50.0     # 感知范围 (单位：米)

# 起点和目标点配置
# SCENARIOS = [
#     (np.array([0.0, 0.0, 0.0]), np.array([200.0, 200.0, 200.0])),
#     (np.array([0.0, 200.0, 0.0]), np.array([200.0, 0.0, 200.0])),
#     (np.array([100.0, 0.0, 0.0]), np.array([100.0, 200.0, 200.0]))
# ]
SCENARIOS = [
    (np.array([0.0, 0.0, 0.0]), np.array([200.0, 200.0, 200.0])),
    (np.array([0.0, 0.0, 0.0]), np.array([200.0, 200.0, 200.0])),
    (np.array([0.0, 0.0, 0.0]), np.array([200.0, 200.0, 200.0]))
]
# SCENARIOS = [
#     (np.array([0.0, 0.0, 0.0]), np.array([1000.0, 1000.0, 1000.0])),
#     (np.array([0.0, 1000.0, 0.0]), np.array([1000.0, 0.0, 1000.0])),
#     (np.array([500.0, 0.0, 0.0]), np.array([200.0, 200.0, 1000.0]))
# ]

# 其他配置项可以根据需要添加
