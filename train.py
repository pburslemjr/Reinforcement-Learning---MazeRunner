import gym


from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from mazerunner import MazeEnv
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H-%M")



TIME_LIMIT = 1000
env = MazeEnv(nice_render = True, time_limit = TIME_LIMIT)

model = PPO("CnnPolicy", env, verbose=1, clip_range=0.1, batch_size=TIME_LIMIT, n_steps=TIME_LIMIT)
model.learn(total_timesteps=TIME_LIMIT*1000)
model.save("ppo-model-" + str(current_time))
