import gym

from stable_baselines3 import DQN

from mazerunner import MazeEnv

import sys

TIME_LIMIT = 500
name = input("Filename")
nr = len(sys.argv) >= 2

env = MazeEnv(nice_render = nr, time_limit = TIME_LIMIT)

model = DQN.load("DQN_maze_runner" + str(name), env=env)
model.learn(total_timesteps=TIME_LIMIT*900)
model.save("DQN_maze_runner" + str(name))


