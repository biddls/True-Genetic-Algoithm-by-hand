import numpy as np


# this class holds a layer of an AI agent, these are chained together in arrays to create a full NN
class layer:
    def __init__(self, inShape, outShape, weights, bias, acti):
        # this holds basic attributes about the layer
        self.inShape: int = inShape
        self.outShape: int = outShape
        self.weights: np.array = weights
        self.bias: np.array = bias
        self.activation = acti

    # this is a function that is useful for debugging as it returns a nicely formatted string telling be about the layer
    def __repr__(self):
        return 'Layer of size: ({}|{})'.format(self.inShape, self.outShape)

    # this is the function that performs inference on what ever matrix is passed in
    # this is done as part of the feed forward algorithm
    def infer(self, arr):
        arr = np.matmul(arr, self.weights)  # multiply the input matrix by the weights
        arr += self.bias  # add the bias
        arr = np.array([[self.activation(x) for x in arr[0]]])  # pass the output through the activation function
        return arr
