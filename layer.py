import numpy as np

# activation function list
# liner
# leaky relu
# sigmoid

class layer:
    def __init__(self, inShape, outShape, weights, bias, acti):
        self.inShape: int = inShape
        self.outShape: int = outShape
        self.weights: np.array = weights
        self.bias: np.array = bias
        self.activation = acti

    def __repr__(self):
        return 'Layer of size: ({}|{})'.format(self.inShape, self.outShape)

    def infer(self, arr):
        arr = np.matmul(arr, self.weights)
        arr += self.bias
        arr = np.array([[self.activation(x) for x in arr[0]]])
        return arr
