import numpy as np
# from ..environment import Environment
from environment import Environment

class MASAC:
    def __init__(self, env: Environment):
        self.env = env

    def plan_path(self, start, goal):
        path = [np.array(start)]
        current = np.array(start)
        velocity = np.zeros(3)
        dt = 0.1
        max_speed = 5.0
        max_acc = 2.0
        while np.linalg.norm(current - goal) > 0.1:
            desired_vel = (goal - current) * 2
            acc = np.clip(desired_vel - velocity, -max_acc, max_acc)
            velocity += acc * dt
            speed = np.linalg.norm(velocity)
            if speed > max_speed:
                velocity = velocity / speed * max_speed
            next_pos = current + velocity * dt
            if not self.env.is_collision(next_pos):
                current = next_pos
            else:
                avoid_dir = self.get_avoid_direction(current)
                current += avoid_dir * 2
                velocity = np.zeros(3)
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