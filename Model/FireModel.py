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

    def isFireDone(self):
        for i in range(0, len(self.fireMap)):
            for j in range(0, len(self.fireMap[i])):
                if self.fireMap[i][j] == self.BURNING:
                    return False
        return True