import gym

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from mazerunner import MazeEnv



TIME_LIMIT = 1000
env = MazeEnv(nice_render = False, time_limit = TIME_LIMIT)

model = PPO("CnnPolicy", env, verbose=1, batch_size=TIME_LIMIT, n_steps=TIME_LIMIT)
model.learn(total_timesteps=TIME_LIMIT*10000)
model.save("testMod")
