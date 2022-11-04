import numpy as np
import random
import EcoModel
import FireModel
import WindModel

class CombustionModel():
    def __init__(self, n, m, seed):
        self.n = n
        self.m = m
        self.seed = seed
        np.random.seed(self.seed)
        random.seed(self.seed)

        self.EcoModel = EcoModel(self.n, self.m, self.seed)
        self.FireModel = FireModel(self.n, self.m, self.seed)
        self.WindModel = WindModel(self.n, self.m, self.seed)

        self.generate_spread_map()
        
    
    def generate_spread_map(self):
        self.spreadMap = np.array(np.random.rand(self.n, self.m))
        return