from random import random
from random import choice
from model import model
from util import pairs
from env import start



# this class holds all the code for the breading of 2 agents his includes mixing of DNA
# to create their offspring and genetic variation
class breeder:
    def __init__(self, agents, noOfSplits=20, mutation=0.01):
        self.agents = agents
        self.genomeLen = None

        # This ensures that the agents have 'compatible' DNA
        if self.agents[0].shape == self.agents[1].shape and len(self.agents[0].genome) == len(self.agents[1].genome):
            self.genomeLen = len(self.agents[0].genome)  # sets the length of the genome sequence
            # generates a list of split locations randomly for interchanging of DNA
            noOfSplits = sorted([round(random() * (self.genomeLen - 3)) + 2 for x in range(noOfSplits - 2)])
            # adds some padding to the list to allow it to work more robustly
            noOfSplits.insert(0, 0)
            noOfSplits.insert(-1, len(self.agents[0].genome))
            # this generates the new genome sequence using list segmentation to mix and match the strings
            # together by the splits generated earlier
            child = ''.join(
                [choice([x.genome[pair[0]:pair[1]] for x in self.agents]) for pair in pairs(noOfSplits)])
            oppo = {'0': '1',
                    '1': '0'}
            # some genes will be swapped randomly using the dictionary above
            child = ''.join([oppo[x] if random() <= mutation else x for x in child])
            # the newly breeded child is then sent off to tests its value
            self.child = model()
            self.child.parseIn(agents[0].shape+','+child)
            start(agents[0].shape, mdl=self.child)
        else:
            # returns an error message if the parents arnt compatible
            print("ERROR shapes dont match")


# test script for the code abover
if __name__ == '__main__':
    m = model()
    m.initMdl(['4li', '5le', '6si'])
    d = model()
    d.initMdl(['4li', '5le', '6si'])
    b = breeder([m, d], 20)
    print(m.genome)
    print(b.child)
    print(d.genome)
