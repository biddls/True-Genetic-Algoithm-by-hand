import numpy as np

class layer:
    def __init__(self, inShape, outShape, weights, bias):
        self.inShape: int = inShape
        self.outShape: int = outShape
        self.weights: np.array = weights
        self.bias: np.array = bias


