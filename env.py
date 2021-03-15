from model import model
import numpy as np
import gym


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
            if done:
                break
    # closes the env
    env.close()
    # saves the agents with its new score
    m.end()