import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.dirname(__file__))

import numpy as np
import sys
import random
from EcoModel import EcoModel
from FireModel import FireModel
from WindModel import WindModel
from DroneModel import DroneModel

class CombustionModel():
    def __init__(self, n, m, seed, isPredictionMode):
        self.n = n
        self.m = m
        self.seed = seed
        self.isPredictionMode = isPredictionMode
        np.random.seed(self.seed)
        random.seed(self.seed)

        # init models
        self.EcoModel = EcoModel(self.n, self.m, self.seed)
        self.FireModel = FireModel(self.n, self.m, self.seed)
        self.WindModel = WindModel(self.n, self.m, self.seed)

        # generate terrain
        self.EcoModel.generate_terrain()
        # generate spread map
        self.generate_spread_map()
        
        self.DroneModel = DroneModel(self.n, self.m, self.seed, self.spreadMap, self.FireModel.fireMap, 2)
        self.DroneModel.initialize()

    
    def generate_spread_map(self):
        self.spreadMap = np.zeros((self.n,self.m), dtype=float)
        for i in range(0, len(self.spreadMap)):
            for j in range(0, len(self.spreadMap[i])):
                self.spreadMap[i][j] = self.EcoModel.get_spread_rate(i, j) * self.WindModel.windSpeed


    def spread(self):
        # one spread call equals 42.6 seconds real time
        spread = []
        for i in range(0, len(self.FireModel.fireMap)):
            for j in range(0, len(self.FireModel.fireMap[i])):
                if self.FireModel.fireMap[i][j] == self.FireModel.BURNING and self.spreadMap[i][j] >= 1:
                    neighbors = self.get_neighbourhood(1, i, j, self.spreadMap)
                    for k in range(0, len(neighbors)):
                        for l in range(0, len(neighbors[k])):
                            if i+(k-1) >= 0 and i+(k-1) < self.n and j+l-1 >= 0 and j+l-1 < self.m:
                                    if self.spreadMap[i+k-1][j+l-1] > 0 and self.FireModel.fireMap[i+k-1][j+l-1] == self.FireModel.UNBURNED:
                                        spread.append((i+k-1,j+l-1))
        for pair in spread:
            self.FireModel.start_fire(pair[0], pair[1])
        
        self.DroneModel.move()
        #print("spreadModel: ", self.DroneModel.noisySpreadMap[0])
        return

    def burn_down(self):
        return

    def get_neighbourhood_with_wind(self, row_number, column_number, map):
        if self.WindModel.windDirection == self.WindModel.NONE:
            return self.get_neighbourhood(1, row_number, column_number, map)
        elif self.WindModel.windDirection == self.WindModel.N:
            return [[map[i][j] if  i >= 0 and i < len(map) and j >= 0 and j < len(map[0]) else 0
            for j in range(column_number-1, column_number+2)]
                for i in range(row_number-1, row_number)]

    def get_neighbourhood(self, radius, row_number, column_number, map):
        return [[map[i][j] if  i >= 0 and i < len(map) and j >= 0 and j < len(map[0]) else 0
            for j in range(column_number-1-radius, column_number+radius)]
                for i in range(row_number-1-radius, row_number+radius)]

    def get_terrainMap(self):
        return self.EcoModel.terrainMap

if __name__=="__main__":
    np.set_printoptions(threshold=sys.maxsize)
    test_model = CombustionModel(n=32, m=32, seed=1, isPredictionMode=False)
    test_model.FireModel.start_fire(int(test_model.n/2), int(test_model.m/2))
    #print(test_model.spreadMap[0])
    #test_model.spread()

