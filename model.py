import time
import os
import sys
import numpy as np
from util import pairs
from gray import gray
from layer import layer
from random import choice
from activations import activations


# this class handles the loading, storing and inference for any given AI in this project
class model:
    def __init__(self):
        self.genome = None
        self.shape = None
        self.grayNumb = None
        self.layers = []
        self.score = 0

    # loads in the txt file into a mdl
    def loadFile(self, path: str):
        f = open(path, "r")
        f = f.readline().replace('\n','')
        self.parseIn(f, path)

    # saves the model used by the end function
    def save(self, path: str):
        temp: str = self.shape + ',' + self.genome
        with open(path, 'w') as f:
            f.write(temp)

    # this handles the parsing in of the text file
    def parseIn(self, f, path=None):
        try:
            # splits it into the model shape and the models genome
            f = f.split(',')
            # writes the shape
            self.shape = f[0]
            # splits up the AI to parse int the shape of the model to be used later
            f[0] = [[int(x[:-2]), x[-2:]] for x in f[0].split('-')]
            # writes the genome to a class variable
            self.genome = f[1]
            # splits up the genome into sections of 8, these sections of 8 represent the 8 bits held for each number
            f[1] = [f[1][i:i + 8] for i in range(0, len(f[1]), 8)]
            # converts them into numbers from the genome
            self.grayNumb = [gray(x, str) for x in f[1]]
            f[1] = [number.numb() for number in self.grayNumb]
            # 1XN x NX(N+1) for formatting of matrices
            # uses the generator function to go though the modle ot initliase all of the layers
            for x in pairs(f[0]):
                # sets the activation function
                acti = activations.get(x[0][1])
                # finds the length of the matrix for the weights if it was flatted into a 1D vector
                lenOfMat: int = x[0][0] * x[1][0]
                # this cuts out that section of the genome into the weight vector and leaves the rest of the genome
                weight, f[1] = f[1][:lenOfMat], f[1][lenOfMat:]
                # this reshapes the matrix into a 2D array
                weight = np.array(weight)
                weight = np.reshape(weight, (x[0][0], x[1][0]))
                # this cuts out the length of the string needed for the bias term
                bias, f[1] = f[1][:x[1][0]], f[1][x[1][0]:]
                # this reshapes the matrix into a 1 by n array
                bias = np.array(bias)
                bias = np.reshape(bias, (1, x[1][0]))
                # this initialises the layer class which is appended to the agents
                self.layers.append(layer(x[0][0], x[1][0], weight, bias, acti))
        except Exception as inst:
            if path is not None:
                os.remove(path)
            else:
                print(type(inst))  # the exception instance
                print(inst.args)  # arguments stored in .args
                print(inst)
            sys.exit()

    # initialised a random model
    def initMdl(self, shape):
        temp: str = ''
        for pair in pairs(shape):
            # generates a random list of 1s and 0s
            temp += ''.join([str(choice([0, 1])) for x in range(((int(pair[0][:-2]) + 1) * int(pair[1][:-2]))*8)])

        # it parses in the string to be turned into a model
        self.parseIn('-'.join([str(x) for x in shape]) + ',' + temp)
        self.layers = self.layers[-len(shape)+1:]

    # runs the inference on the env observation
    def inference(self, arr):
        for x in self.layers:
            arr = x.infer(arr)
        return arr

    # saves the AI as a text file
    def end(self):
        self.save('agents\\{}.txt'.format(self.score))


# test script
if __name__ == '__main__':
    m = model()
    m.initMdl(['4li', '5le', '6si'])
    a = [[1, 1, 1, 1]]
    print(m.inference(np.array(a)))
