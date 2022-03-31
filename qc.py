import gym

from stable_baselines3 import DQN

from mazerunner import MazeEnv


TIME_LIMIT = 2048

env = MazeEnv(nice_render = True, time_limit = TIME_LIMIT)

model = DQN.load("test", env=env)
print(str(model.exploration_final_eps))
model.exploration_final_eps = 0.8
print(str(model.exploration_final_eps))
model.learn(total_timesteps=TIME_LIMIT*20000)
model.save("DQN_maze_runner")


