import numpy as np
import random

class WilfireModel():
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.spreadMap = np.random.rand(self.n, self.m)
        self.fireMap = np.zeros((self.n,self.m), dtype=int)
    
model = WilfireModel(5,5)
print(model.spreadMap)