import numpy as np
import random

class FireModel():
    def __init__(self, n, m, seed):
        self.n = n
        self.m = m
        self.seed = seed
        np.random.seed(self.seed)
        random.seed(self.seed)
        self.fireMap = np.zeros((self.n,self.m), dtype=int)