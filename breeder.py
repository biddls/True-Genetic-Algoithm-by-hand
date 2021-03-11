from random import random
from random import choice
from model import model
from util import pairs


class breeder:
    def __init__(self, agents, noOfSplits, mutation=0):
        self.agents = agents
        self.genomeLen = None
        self.child = None
        # print(self.agents)

        if self.agents[0].shape == self.agents[1].shape and len(self.agents[0].genome) == len(self.agents[1].genome):
            self.genomeLen = len(self.agents[0].genome)
            noOfSplits = sorted([round(random() * (self.genomeLen - 3)) + 2 for x in range(noOfSplits-2)])
            noOfSplits.insert(0, 0)
            noOfSplits.insert(-1, len(self.agents[0].genome))
            self.child = ''.join([choice([x.genome[pair[0]:pair[1]] for x in self.agents]) for pair in pairs(noOfSplits)])
            oppo = {'0': '1',
                    '1': '0'}
            self.child = ''.join([oppo[x] if random() <= 0.01 else x for x in self.child])
        else:
            print("ERROR shapes dont match")


if __name__ == '__main__':
    m = model()
    m.initMdl(['4li', '5le', '6si'])
    d = model()
    d.initMdl(['4li', '5le', '6si'])
    b = breeder([m, d], 20)
    print(m.genome)
    print(b.child)
    print(d.genome)
