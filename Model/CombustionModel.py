import numpy as np
import random
import EcoModel
import FireModel
import WindModel

class CombustionModel():
    def __init__(self, n, m, seed, isPredictionMode):
        self.n = n
        self.m = m
        self.seed = seed
        self.isPredictionMode = isPredictionMode
        np.random.seed(self.seed)
        random.seed(self.seed)

        self.EcoModel = EcoModel(self.n, self.m, self.seed)
        self.FireModel = FireModel(self.n, self.m, self.seed)
        self.WindModel = WindModel(self.n, self.m, self.seed)

        self.generate_spread_map()
        
    
    def generate_spread_map(self):
        self.spreadMap = np.zeros((self.n,self.m), dtype=int)
        for i in range(0, len(self.spreadMap)):
            for j in range(0, len(self.spreadMap[i])):
                self.spreadMap[i][j] = self.EcoModel.get_spread(self.TerrainMap[i][j]) * self.WindModel.windSpeed


    def spread(self):
        return

    def get_neighbourhood_with_wind(self, row_number, column_number, map):
        return

    def get_neighbourhood(self, radius, row_number, column_number, map):
        return [[map[i][j] if  i >= 0 and i < len(map) and j >= 0 and j < len(map[0]) else 0
            for j in range(column_number-1-radius, column_number+radius)]
                for i in range(row_number-1-radius, row_number+radius)]

    def get_neighbour_spread_risk(self, neighbors):
        highest_wind = 1
        for i in range(0, len(neighbors)):
            for j in range(0, len(neighbors[i])):
                if neighbors[i][j] == 1:
                    if self.wind_coefficient(i-1,j-1) > highest_wind:
                        highest_wind = self.wind_coefficient(i-1,j-1)
        return highest_wind