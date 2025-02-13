import numpy as np
import random
import logging

# Environment configuration
OBSTACLE_DISTRIBUTION = {
    'dispersion_factor': 3.0,
    'overlap_tolerance': 'none',
    'shapes': {
        'cube': 0.4,
        'cylinder': 0.3,
        'sphere': 0.3
    }
}

OBSTACLE_OPACITY = 0.3
OBSTACLE_SHAPES = ['cube', 'cylinder', 'sphere']

logger = logging.getLogger(__name__)

class Environment:
    def __init__(self, size=None, num_obstacles=None):
        """Initialize environment with configurable parameters"""
        self.size = np.array(size if size is not None else [200, 200, 100], dtype=np.float64)
        self.num_obstacles = num_obstacles if num_obstacles is not None else 10
        self.dispersion_factor = 2.0  # Reduced from 3.0 for better obstacle placement
        self.overlap_tolerance = OBSTACLE_DISTRIBUTION['overlap_tolerance']
        self.opacity = OBSTACLE_OPACITY
        self.shapes = OBSTACLE_SHAPES
        self.obstacles = []
        self.generate_obstacles()

    def generate_obstacles(self):
        """Generate obstacles with various shapes and sizes"""
        max_attempts = 50  # Maximum attempts per obstacle generation

        for _ in range(self.num_obstacles):
            for attempt in range(max_attempts):
                x = random.uniform(0, self.size[0])
                y = random.uniform(0, self.size[1])
                z = random.uniform(0, self.size[2])
                size = random.uniform(10.0, 25.0)

                # 随机选择障碍物形状
                shape = random.choices(
                    self.shapes,
                    weights=[OBSTACLE_DISTRIBUTION['shapes'][s] for s in self.shapes]
                )[0]
                
                # 根据形状生成尺寸
                if shape == 'cylinder':
                    a = b = size  # 圆柱体底面半径
                    c = size * random.uniform(2.0, 4.0)  # 圆柱体高度
                elif shape == 'cube':
                    a = b = c = size  # 立方体边长相等
                else:  # sphere
                    a = b = c = size  # 球体半径相等

                theta = random.uniform(0, 2 * np.pi)
                new_obstacle = (x, y, z, a, b, c, theta, shape)

                # 检查新障碍物与现有障碍物的距离
                too_close = False
                for ox, oy, oz, oa, ob, oc, _, _ in self.obstacles:
                    distance = np.linalg.norm([x - ox, y - oy, z - oz])
                    min_distance = self.dispersion_factor * max(a, b, c, oa, ob, oc)
                    if distance < min_distance:
                        too_close = True
                        if self.overlap_tolerance == 'none':
                            break
                        elif self.overlap_tolerance == 'low' and distance < 0.8 * min_distance:
                            break

                if not too_close:
                    self.obstacles.append(new_obstacle)
                    break
            else:
                logger.warning("Failed to place obstacle at reasonable distance, skipping obstacle")

    def is_collision(self, point):
        """Check if point collides with any obstacle"""
        point = np.array(point)
        for x, y, z, a, b, c, theta, shape in self.obstacles:
            rot_matrix = np.array([
                [np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1]
            ])
            rel_point = rot_matrix @ (point - np.array([x, y, z]))

            if shape == 'sphere':
                if np.sum((rel_point / a) ** 2) <= 1:
                    return True
            elif shape == 'cylinder':
                if (rel_point[0] / a) ** 2 + (rel_point[1] / b) ** 2 <= 1 and abs(rel_point[2]) <= c/2:
                    return True
            elif shape == 'cube':
                if all(abs(rel_point[i]) <= dim/2 for i, dim in enumerate([a, b, c])):
                    return True

        return False

    def render(self):
        """Simple rendering method"""
        for obstacle in self.obstacles:
            print(f"Obstacle: {obstacle}, Opacity: {'Transparent' if self.opacity else 'Opaque'}")

def calculate_metrics(path, env):
    """Calculate path metrics"""
    length = sum(np.linalg.norm(path[i + 1] - path[i]) for i in range(len(path) - 1))
    collisions = sum(env.is_collision(point) for point in path)
    flight_time = len(path) * 0.1  # 每个点之间的飞行时间为0.1秒
    turning_points = calculate_turning_points(path)
    return {
        '路径长度': length,
        '碰撞次数': collisions,
        '飞行时间': flight_time,
        '转折点数': turning_points
    }

def calculate_turning_points(path):
    """Calculate number of turning points in path"""
    turning_points = 0
    for i in range(1, len(path) - 1):
        v1 = path[i] - path[i - 1]
        v2 = path[i + 1] - path[i]
        if np.linalg.norm(v1) * np.linalg.norm(v2) > 1e-6:
            if np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)) < 0.99:
                turning_points += 1
    return turning_points

def setup_environment(size=(200.0, 200.0, 200.0), num_obstacles=20):
    """Setup environment with default parameters"""
    env = Environment(size, num_obstacles)
    print("环境已创建")
    env.render()
    return env
