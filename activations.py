import numpy as np

# activation function list
# linear
# leaky relu
# sigmoid

activations = {"li": lambda x: x,
               "le": lambda x: max(x * 0.01, x),
               "si": lambda x: 1 / (1 + np.exp(-x))}
