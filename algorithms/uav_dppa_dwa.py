import numpy as np
# from ..environment import Environment
from environment import Environment

class UAV_DPPA_DWA:
    def __init__(self, env: Environment):
        self.env = env

    def plan_path(self, start, goal):
        path = [np.array(start)]
        current = np.array(start)
        while np.linalg.norm(current - goal) > 0.1:
            direction = (goal - current) / np.linalg.norm(goal - current)
            step_size = min(float(5), float(np.linalg.norm(goal - current)))
            next_pos = current + direction * step_size
            if not self.env.is_collision(next_pos):
                current = next_pos
            else:
                avoid_dir = self.get_avoid_direction(current)
                current += avoid_dir * 2
            path.append(current)
        path.append(goal)
        return np.array(path)

    def get_avoid_direction(self, point):
        for _ in range(20):
            avoid_dir = np.random.randn(3)
            avoid_dir /= np.linalg.norm(avoid_dir)
            if not self.env.is_collision(point + avoid_dir * 2):
                return avoid_dir
        return np.random.randn(3)
