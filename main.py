# s[0] is the horizontal coordinate
# s[1] is the vertical coordinate
# s[2] is the horizontal speed
# s[3] is the vertical speed
# s[4] is the angle
# s[5] is the angular speed
# s[6] 1 if first leg has contact, else 0
# s[7] 1 if second leg has contact, else 0

import threading
import time
import os
from model import model
import gym
import numpy as np
from util import codeTimer
from util import pairs
from breeder import breeder


def start(shape, path=None, mdl=None):
    if mdl is None:
        if path is None:
            m = model()
            m.initMdl(shape)
        else:
            m = model()
            m.loadFile(path)
    else:
        m = mdl

    env = gym.make('LunarLander-v2')
    for i_episode in range(5):
        observation = env.reset()  # resets the env
        for t in range(200):
            action = np.argmax(m.inference(observation.reshape((1, 8))))
            # 0 is nothing
            # 1 is left fire
            # 2 is bottom fire
            # 3 is right fire
            observation, reward, done, info = env.step(action)  # sends the action to the env and gets back info
            m.score += reward
            if done:
                break
    env.close()
    m.end()


def breed(dir):
    dirLi = os.listdir(dir)
    # print(len(dirLi))
    for index, pair in enumerate(dirLi[:-2:2]):
        # print(index)
        temp = [model(), model()]
        temp[0].loadFile(dir + '\\' + pair)
        temp[1].loadFile(dir + '\\' + (dirLi[(index * 2) + 1]))
        # print(temp[0] == temp[1])
        child = breeder(temp, 20).child
        m = model()
        m.parseIn(temp[0].shape+','+child)
        start(temp[0].shape, mdl=m)


def watch(checkIn, total):
    while threading.active_count() > 1:
        temp1 = threading.active_count()
        time.sleep(checkIn)
        temp2 = threading.active_count()
        print('seconds remaining: {}, threads left: {}'.format(round((total/(total if (temp1 - temp2) == 0 else (temp1 - temp2)))*checkIn), temp2))


if __name__ == '__main__':
    populationSize = 100
    threads = []
    checkIn = 2
    shape = ['8li', '10le', '4si']
    dir = 'agents'

    while 1:
        noOfAgents = len(os.listdir(dir))
        if noOfAgents >= 2:
            print('the number of agents is: {} and the max agent is: {}'.format(noOfAgents, max(os.listdir(dir), key=lambda x: float(x[:-4]))))

        if noOfAgents > populationSize:  # trim
            print('Cull the weak')
            a = os.listdir(dir)
            a.sort(key=lambda x: float(x[:-4]), reverse=True)
            [os.remove(dir+'\\'+file) for file in a[populationSize:]]

        elif noOfAgents == populationSize:  # evaluate and then breed
            print('test mdls then breed them')
            agents = os.listdir(dir)
            for x in agents:
                threading.Thread(target=start, args=[shape, dir+'\\'+x]).start()

            # watch(checkIn, populationSize)
            breed(dir)

        else:  # make new ones to catch up
            print('make new ones to catch up')
            while len(os.listdir(dir)) < populationSize:
                needed = populationSize - len(os.listdir(dir))
                for x in range(needed):
                    threading.Thread(target=start, args=[shape]).start()
                # watch(checkIn, needed)
                breed(dir)
