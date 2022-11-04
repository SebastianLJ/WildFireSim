import numpy as np
import random

class DroneModel():
    def __init__(self, n, m, seed, spreadMap, noisySpreadMap):
        self.n = n
        self.m = m
        self.seed = seed
        np.random.seed(self.seed)
        random.seed(self.seed)
        self.spreadMap = spreadMap
        self.noisySpreadMap = noisySpreadMap
        self.droneMap = np.zeros((self.n,self.m), dtype=int)