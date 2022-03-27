import gym

import sys
from stable_baselines3 import DQN
from mazerunner import MazeEnv



env = MazeEnv(nice_render = True)
if (len(sys.argv) <= 1):
    print("Specify model Filename!")
    quit()
model_name = str(sys.argv[1])
model = DQN.load(model_name)
obs = env.reset()
while True:
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    print(str(reward))
    env.render()
    if done:
      obs = env.reset()
