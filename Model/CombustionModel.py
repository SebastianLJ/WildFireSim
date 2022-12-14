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
from Log import Log

class CombustionModel():
    def __init__(self, n, m, seed, isPredictionMode=False, droneCount=0):
        # cell size is 30m
        self.n = n
        self.m = m
        self.seed = seed
        self.time = 0
        self.isPredictionMode = isPredictionMode
        self.droneCount = droneCount
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
        self.burnDownMap = np.zeros((self.n,self.m), dtype=float)
        self.burnDownMap.fill(30*30)
        
        if self.isPredictionMode:
            self.DroneModel = DroneModel(self.n, self.m, self.seed, self.spreadMap, self.FireModel.fireMap, self.droneCount)
            self.DroneModel.initialize()

    
    def generate_spread_map(self):
        self.spreadMap = np.zeros((self.n,self.m), dtype=float)
        for i in range(0, len(self.spreadMap)):
            for j in range(0, len(self.spreadMap[i])):
                self.spreadMap[i][j] = self.EcoModel.get_spread_rate(i, j) * self.WindModel.windSpeed


    def spread(self, trueSpreadMap = [[0,0],[0,0]]):
        # one spread call equals 27.307 seconds real time
        spread = []
        for i in range(0, len(self.FireModel.fireMap)):
            for j in range(0, len(self.FireModel.fireMap[i])):
                if self.FireModel.fireMap[i][j] == self.FireModel.BURNING and self.spreadMap[i][j] >= 1:
                    mask = self.get_neighbourhood_mask(i, j, self.WindModel.get_wind_radius(), self.spreadMap)
                    # continue if no unburnt cells in neighbourhood
                    if np.count_nonzero(self.FireModel.fireMap[mask]) == self.FireModel.fireMap[mask].size:
                        continue
                    for k in range(0, self.n):
                        for l in range(0, self.m):
                            if (mask[k][l] and self.spreadMap[k][l] > 0 and 
                                self.angle_in_range(self.get_angle(j, i, l, k), self.WindModel.get_wind_angle_min(), self.WindModel.get_wind_angle_max()) and
                                self.FireModel.fireMap[k][l] == self.FireModel.UNBURNT):
                                    spread.append([k,l])
                elif self.FireModel.fireMap[i][j] == self.FireModel.BURNING:
                    self.spreadMap[i][j] += (self.EcoModel.get_spread_rate(i, j) * self.WindModel.windSpeed)
        for pair in spread:
            self.FireModel.start_fire(pair[0], pair[1])
        self.burn_down()
        if self.isPredictionMode:
            self.DroneModel.move(trueSpreadMap)
            self.spreadMap = self.DroneModel.noisySpreadMap
        self.time += 27.3
        return self.time

    def burn_down(self):
        for i in range(0, self.n):
            for j in range(0, self.m):
                if self.FireModel.fireMap[i][j] == self.FireModel.BURNING and self.burnDownMap[i][j] > 0:
                    # windspeed is normalized to 0-10
                    self.burnDownMap[i][j] -= self.EcoModel.get_burn_rate(i, j) * (self.WindModel.windSpeed * 10)
                    if self.burnDownMap[i][j] <= 0:
                        self.FireModel.fireMap[i][j] = self.FireModel.BURNT
                        self.burnDownMap[i][j] = 0

    def get_neighbourhood_mask(self, row_number, column_number, radius, map):
        x = np.arange(0, self.m)
        y = np.arange(0, self.n)
        mask = ((x[np.newaxis,:]-column_number)**2 + (y[:,np.newaxis]-row_number)**2 < radius**2)
        return mask

    def angle_in_range(self, angle, lower, upper):
        return (angle - lower) % 360 <= (upper - lower) % 360 or lower == upper

    def get_angle(self, cx, cy, px, py):
        dx = px - cx
        dy = py - cy
        rads = np.arctan2(dy,dx)
        rads %= 2*np.pi
        degs = np.degrees(rads)
        return degs

    def get_terrainMap(self):
        return self.EcoModel.terrainMap

    def set_start_fire(self, i, j):
        if self.EcoModel.get_spread_rate(i, j) > 0:
            self.FireModel.start_fire(i, j)
        else:
            raise Exception("Cannot start fire on water or earth")
        

if __name__=="__main__":
    np.set_printoptions(threshold=sys.maxsize)
    test_model = CombustionModel(n=32, m=32, seed=1, isPredictionMode=False)
    test_model.FireModel.start_fire(int(test_model.n/2), int(test_model.m/2))
    print(test_model.get_angle(1,1,2,1))

