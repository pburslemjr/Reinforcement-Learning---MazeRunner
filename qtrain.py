import gym

from stable_baselines3 import DQN

from mazerunner import MazeEnv


TIME_LIMIT = 1000

env = MazeEnv(nice_render = True, time_limit = TIME_LIMIT)

model = DQN("MlpPolicy", env, exploration_fraction=0.9, verbose=1)
model.learn(total_timesteps=TIME_LIMIT*1000)
model.save("DQN_maze_runner")


