import os
import sys

import numpy as np
import util
from gray import gray
from layer import layer
from random import choice
from activations import activations

class model:
    def __init__(self):
        self.genome = None
        self.shape = None
        self.grayNumb = None
        self.layers = []
        self.score = 0

    def loadFile(self, path: str):
        f = open(path, "r")
        f = f.readline().replace('\n','')
        self.parseIn(f, path)

    def save(self, path: str):
        temp: str = self.shape + ',' + self.genome
        with open(path, 'w') as f:
            f.write(temp)

    def parseIn(self, f, path=None):
        try:
            f = f.split(',')
            self.shape = f[0]
            f[0] = [[int(x[:-2]), x[-2:]] for x in f[0].split('-')]
            self.genome = f[1]
            f[1] = [f[1][i:i + 8] for i in range(0, len(f[1]), 8)]
            self.grayNumb = [gray(x, str) for x in f[1]]
            f[1] = [number.numb() for number in self.grayNumb]
            # 1XN x NX(N+1) for formatting of matracies
            for x in util.pairs(f[0]):
                acti = activations.get(x[0][1])
                lenOfMat: int = x[0][0] * x[1][0]
                weight, f[1] = f[1][:lenOfMat], f[1][lenOfMat:]
                weight = np.array(weight)
                weight = np.reshape(weight, (x[0][0], x[1][0]))
                bias, f[1] = f[1][:x[1][0]], f[1][x[1][0]:]
                bias = np.array(bias)
                bias = np.reshape(bias, (1, x[1][0]))
                self.layers.append(layer(x[0][0], x[1][0], weight, bias, acti))
        except Exception as inst:
            if path is not None:
                os.remove(path)
            else:
                print(type(inst))  # the exception instance
                print(inst.args)  # arguments stored in .args
                print(inst)
            sys.exit()

    def initMdl(self, shape):
        temp: str = ''
        for pair in util.pairs(shape):
            temp += ''.join([str(choice([0, 1])) for x in range(((int(pair[0][:-2]) + 1) * int(pair[1][:-2]))*8)])

        self.parseIn('-'.join([str(x) for x in shape]) + ',' + temp)
        self.layers = self.layers[-len(shape)+1:]

    def inference(self, arr):
        for x in self.layers:
            arr = x.infer(arr)
        return arr

    def end(self):
        self.save('agents\\{}.txt'.format(self.score))

if __name__ == '__main__':
    m = model()
    m.initMdl(['4li', '5le', '6si'])
    a = [[1, 1, 1, 1]]
    print(m.inference(np.array(a)))
