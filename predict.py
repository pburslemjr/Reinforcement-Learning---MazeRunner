import gym

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from mazerunner import MazeEnv



env = MazeEnv(nice_render = True)

model = PPO.load("testMod")
obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    if dones:
        env.reset()
