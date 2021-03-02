path = 'agents\\1123.0281698915778.txt'


import gym
import numpy as np
from model import model


m = model()
m.loadFile(path)
env = gym.make('LunarLander-v2')
for i_episode in range(50):
    observation = env.reset()  # resets the env
    for t in range(200):
        env.render()
        action = np.argmax(m.inference(observation.reshape((1, 8))))
        # 0 is nothing
        # 1 is left fire
        # 2 is bottom fire
        # 3 is right fire
        observation, reward, done, info = env.step(action)  # sends the action to the env and gets back info
        m.score += reward
        if done:
            break