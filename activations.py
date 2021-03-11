import numpy as np

# activation function list
# linear
# leaky relu
# sigmoid

# this is just a list of all the activations available to the AI
activations = {"li": lambda x: x,
               "le": lambda x: max(x * 0.01, x),
               "si": lambda x: 1 / (1 + np.exp(-x))}
