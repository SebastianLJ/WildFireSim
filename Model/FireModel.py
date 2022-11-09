import numpy as np
import random

class FireModel():
    BURNT, UNBURNT, BURNING = -1, 0, 1
    def __init__(self, n, m, seed):
        self.n = n
        self.m = m
        self.seed = seed
        np.random.seed(self.seed)
        random.seed(self.seed)
        self.fireMap = np.zeros((self.n,self.m), dtype=int)

    def start_fire(self, x, y):
        self.fireMap[x][y] = self.BURNING