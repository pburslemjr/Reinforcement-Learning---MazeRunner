import gym

from stable_baselines3 import DQN

from mazerunner import MazeEnv
import sys


name = input("Filename")
TIME_LIMIT = 1000
nr = len(sys.argv) >= 2
env = MazeEnv(nice_render = nr, time_limit = TIME_LIMIT)

model = DQN("CnnPolicy", env, buffer_size=500000, batch_size=1000, optimize_memory_usage=True, exploration_fraction=0.25, verbose=2)
model.learn(total_timesteps=TIME_LIMIT*20000)
model.save("DQN_maze_runner" + str(name))


