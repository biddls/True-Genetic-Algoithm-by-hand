# s[0] is the horizontal coordinate
# s[1] is the vertical coordinate
# s[2] is the horizontal speed
# s[3] is the vertical speed
# s[4] is the angle
# s[5] is the angular speed
# s[6] 1 if first leg has contact, else 0
# s[7] 1 if second leg has contact, else 0

import gym
env = gym.make('LunarLander-v2')
for i_episode in range(1):
    observation = env.reset()  # resets the env
    for t in range(100):
        env.render()  # shows the env
        action = env.action_space.sample()  # chooses action at random
        observation, reward, done, info = env.step(action)  # sends the action to the env and gets back info
        print(observation, reward, done, info)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
env.close()