from tqdm import tqdm
from tqdm import trange
import threading
import os
from model import model
from breeder import breeder
import wanb
import webbrowser
from env import start


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
            itter.set_description(f'breading {pair, dirLi[(index * 2) + 1]} to then test their offspring running across {threading.activeCount()} threads')
            # it breads the pair
            threading.Thread(target=breeder, args=[temp], daemon=True).start()
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
    logging = wanb.wanb("Thu Mar 11 16:08:11 2021['8li', '16le', '8le', '4si']", 0)
    webbrowser.open('https://wandb.ai/thomasbiddlecombe/ga')  # if you want to run it your self
    # you will need to change this url
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        for x in range(100):
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
                # breeds the agents and then tests their children
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
                logging.log(float(a[0][:-4]), (sum(total) / len(total)))


        # at the end of the training it performs a few actions to close down
        os.system('cls' if os.name == 'nt' else 'clear')
        print('#############|Training Stopped|#############')
        logging.end()

    # if it halt the training early it runs through the close down process
    except KeyboardInterrupt:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('#############|Training Stopped|#############')
        logging.end()
