import numpy as np
import random

class EcoModel():

    def __init__(self, n, m, seed):
        self.n = n
        self.m = m
        self.seed = seed
        np.random.seed(self.seed)
        random.seed(self.seed)
        self.terrainMap = np.array(np.random.rand(self.n, self.m))
        self.elevationMap = np.zeros((self.n,self.m), dtype=int)
        self.nonBurnMap = np.zeros((self.n,self.m), dtype=int)