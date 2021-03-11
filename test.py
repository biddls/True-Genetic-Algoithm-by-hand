import gym
import numpy as np
from model import model


def showOff(path):
    m = model()
    m.loadFile(path)
    env = gym.make('LunarLander-v2')
    while 1:
        observation = env.reset()  # resets the env
        for t in range(500):
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


if __name__ == '__main__':
    path = 'agents\\2842.4817334373574.txt'
    showOff(path)
