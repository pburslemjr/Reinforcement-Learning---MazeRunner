import gym

from stable_baselines3 import DQN

from mazerunner import MazeEnv


TIME_LIMIT = 1000

env = MazeEnv(nice_render = True, time_limit = TIME_LIMIT)

model = DQN("MlpPolicy", env, exploration_fraction=0.25, batch_size=1024, verbose=1)
for i in range(10):
    model.learn(total_timesteps=TIME_LIMIT*300, exploration_fraction=0.1*i)
    model.save("DQN_maze_runner" + str(i))


