import gym

from stable_baselines3 import DQN

from mazerunner import MazeEnv


TIME_LIMIT = 2048

env = MazeEnv(nice_render = False, time_limit = TIME_LIMIT)

model = DQN("MlpPolicy", env, exploration_fraction=0.85, exploration_initial_eps=1.0, exploration_final_eps=0.03, gamma=0.99, batch_size=TIME_LIMIT, verbose=2)
model.learn(total_timesteps=TIME_LIMIT*200)
model.save("DQN_maze_runner")


