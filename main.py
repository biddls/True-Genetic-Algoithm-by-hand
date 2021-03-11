# s[0] is the horizontal coordinate
# s[1] is the vertical coordinate
# s[2] is the horizontal speed
# s[3] is the vertical speed
# s[4] is the angle
# s[5] is the angular speed
# s[6] 1 if first leg has contact, else 0
# s[7] 1 if second leg has contact, else 0
import keyboard as keyboard
from tqdm import tqdm
from tqdm import trange
import threading
import time
import os
from model import model
import gym
import numpy as np
from breeder import breeder
import wanb
import webbrowser


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
    for i_episode in range(20):
        observation = env.reset()  # resets the env
        for t in range(500):
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
    with tqdm(total=len(dirLi[:-2:2])) as itter:
        for index, pair in enumerate(dirLi[:-2:2]):
            # print(index)
            temp = [model(), model()]
            temp[0].loadFile(dir + '\\' + pair)
            temp[1].loadFile(dir + '\\' + (dirLi[(index * 2) + 1]))
            itter.set_description(f'breading {pair, dirLi[(index * 2) + 1]} to then test their offspring')
            # print(temp[0] == temp[1])
            child = breeder(temp, 20, 0.01).child
            m = model()
            m.parseIn(temp[0].shape+','+child)
            start(temp[0].shape, mdl=m)
            itter.update(1)
        itter.set_description('Force breeding complete')


def watch(checkIn, total):
    while threading.active_count() > 1:
        temp1 = threading.active_count()
        time.sleep(checkIn)
        temp2 = threading.active_count()
        print('seconds remaining: {}, threads left: {}'.format(round((total/(total if (temp1 - temp2) == 0 else (temp1 - temp2)))*checkIn), temp2))


if __name__ == '__main__':
    populationSize = 1000
    threads = []
    checkIn = 2
    shape = ['8li', '16le', '8le', '4si']
    dir = 'agents'
    rounds = 0
    logging = wanb.wanb(str(time.asctime()) + str(shape))
    webbrowser.open('https://wandb.ai/thomasbiddlecombe/ga')
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        for x in range(10000):
            noOfAgents = len(os.listdir(dir))
            if noOfAgents > populationSize:  # trim
                a = os.listdir(dir)
                a.sort(key=lambda x: float(x[:-4]), reverse=True)
                try:
                    [os.remove(dir+'\\'+file) for file in tqdm(a[populationSize:], desc='culling the weak')]
                except Exception as e:
                    print(e)


            elif noOfAgents == populationSize:  # evaluate and then breed
                agents = os.listdir(dir)
                with tqdm(total=len(agents)) as itter:
                    for x in agents:
                        itter.set_description(f'testing {x} out of {len(agents)}')
                        threading.Thread(target=start, args=[shape, dir+'\\'+x], daemon=True).start()
                        itter.update(1)
                    itter.set_description('Testing complete, now its time to force breed them,'
                                          ' then cull the weak')
                breed(dir)

            else:  # make new ones to catch up
                for x in trange(populationSize - len(os.listdir(dir)), desc='Birthing new creatures for my ritual of'
                                                                            ' selective breading for the AI gods'):
                    threading.Thread(target=start, args=[shape], daemon=True).start()
                breed(dir)

            if rounds == 3:
                os.system('cls' if os.name == 'nt' else 'clear')
                rounds = 0
            else:
                rounds += 1

            if os.listdir(dir) is not None:
                a = os.listdir(dir)
                a.sort(key=lambda x: float(x[:-4]), reverse=True)
                print(f'{a[0]} is the best agent so far')
                total = [float(file[:-4]) for file in a]
                print(f'the average so far is: {sum(total)/ len(total)}')
                wanb.log(float(a[0][:-4]), (sum(total) / len(total)))

        os.system('cls' if os.name == 'nt' else 'clear')
        print('#############|Training Stopped|#############')
        wanb.end()

    except KeyboardInterrupt:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('#############|Training Stopped|#############')
        wanb.end()
