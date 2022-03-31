import gym

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from mazerunner import MazeEnv



TIME_LIMIT = 200*3
env = MazeEnv(nice_render = True, time_limit = TIME_LIMIT)

model = PPO.load("b", env=env)
model.learn(total_timesteps=TIME_LIMIT*1000)
model.save("c")
