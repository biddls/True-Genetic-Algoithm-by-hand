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


# this function, does AI loading or initialisation and then evaluates said AI
def start(shape, path=None, mdl=None):
    if mdl is None:
        if path is None:
            # if no model is given and no path to load one then it makes one
            m = model()
            m.initMdl(shape)
        else:
            # if no model is given but a path to one is given it loads that one in
            m = model()
            m.loadFile(path)
    else:
        # if a model is given it uses that one
        m = mdl

    # init the env
    env = gym.make('LunarLander-v2')
    # the AI has N attempts to land and after which its scores from each
    endE = 20
    endT = 500
    total = 0
    for i_episode in range(endE):
        observation = env.reset()  # resets the env
        for t in range(endT):
            # given the env input it performs an action
            action = np.argmax(m.inference(observation.reshape((1, 8))))
            # this is the list of actions it can make
            # 0 is nothing
            # 1 is left fire
            # 2 is bottom fire
            # 3 is right fire
            # the action is sent to the env and a selection of data is returned
            observation, reward, done, info = env.step(action)  # sends the action to the env and gets back info
            # adds the reward to the models score
            m.score += reward
            # increments the number of time steps taken by the AI
            total += 1
            if done:
                break
    # this encourages the AI to land quickly instead of hovering above the ground in the right position
    # to maximise its points. note with out / by total it learnt to hover in the right position above the landing pad
    # because it got more points that way so im encouraging it to land quickly by punishing it for taking ages to land
    m.score = m.score / total
    # closes the env
    env.close()
    # saves the agents with its new score
    m.end()


# this class manages all of the breeding and evolution
def breed(path):
    dirLi = os.listdir(path)
    # it loads in a list of all the AI
    with tqdm(total=len(dirLi[:-2:2])) as itter:
        for index, pair in enumerate(dirLi[:-2:2]):
            # print(index)
            temp = [model(), model()]
            # it loads in the pair
            temp[0].loadFile(path + '\\' + pair)
            temp[1].loadFile(path + '\\' + (dirLi[(index * 2) + 1]))
            itter.set_description(f'breading {pair, dirLi[(index * 2) + 1]} to then test their offspring')
            # it breads the pair
            child = breeder(temp, 20, 0.01).child
            # creates the model
            m = model()
            m.parseIn(temp[0].shape+','+child)
            # tests the model to see how good it is then saves it
            start(temp[0].shape, mdl=m)
            itter.update(1)
        itter.set_description('Force breeding complete')  # thought it was funny


# this script runs everything and sets up all of the stuff needed for running
if __name__ == '__main__':
    # basic attributes (this code should be in a class but I CBA
    populationSize = 1000
    threads = []
    checkIn = 2
    shape = ['8li', '16le', '8le', '4si']
    dir = 'agents'
    rounds = 0
    # loads up the 'Weights and Bias' service for logging of the AI
    logging = wanb.wanb(str(time.asctime()) + str(shape))
    webbrowser.open('https://wandb.ai/thomasbiddlecombe/ga')  # if you want to run it your self
    # you will need to change this url
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        for x in range(10000):
            noOfAgents = len(os.listdir(dir))
            if noOfAgents > populationSize:  # if there are to many AIs for the max population size then it
                # kills off the weak
                a = os.listdir(dir)
                a.sort(key=lambda x: float(x[:-4]), reverse=True)
                try:
                    [os.remove(dir+'\\'+file) for file in tqdm(a[populationSize:], desc='culling the weak')]
                # some times the threads can get mixed up if stuff takes a while to complete its rare enough to not be an issue
                except Exception as e:
                    print(e)


            elif noOfAgents == populationSize:  # evaluate and then breed the AIs
                agents = os.listdir(dir)
                with tqdm(total=len(agents)) as itter:
                    for x in agents:
                        itter.set_description(f'testing {x} out of {len(agents)}')
                        # it runs the agents to eval them
                        threading.Thread(target=start, args=[shape, dir+'\\'+x], daemon=True).start()
                        itter.update(1)
                    itter.set_description('Testing complete, now its time to force breed them,'
                                          ' then cull the weak')
                # breeds the agents after they have been ranked
                breed(dir)

            else:  # make new ones to catch up
                for x in trange(populationSize - len(os.listdir(dir)), desc='Birthing new creatures for my ritual of'
                                                                            ' selective breading for the AI gods'):
                    # inits new agents if there arnt enough
                    threading.Thread(target=start, args=[shape], daemon=True).start()
                # breeds the agents after they have been initialised and then ranked
                breed(dir)

            if rounds == 3:
                # clears the console after N iterations to keep it tidy enough
                os.system('cls' if os.name == 'nt' else 'clear')
                rounds = 0
            else:
                rounds += 1

            # returns some metrics on the AIs performance
            if os.listdir(dir) is not None:
                a = os.listdir(dir)
                a.sort(key=lambda x: float(x[:-4]), reverse=True)
                print(f'{a[0]} is the best agent so far')
                total = [float(file[:-4]) for file in a]
                print(f'the average so far is: {sum(total)/ len(total)}')
                # logs these metrics with 'Weights and Bias' so i can watch the graph in the browser
                wanb.log(float(a[0][:-4]), (sum(total) / len(total)))

        # at the end of the training it performs a few actions to close down
        os.system('cls' if os.name == 'nt' else 'clear')
        print('#############|Training Stopped|#############')
        wanb.end()

    # if it halt the training early it runs through the close down process
    except KeyboardInterrupt:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('#############|Training Stopped|#############')
        wanb.end()
