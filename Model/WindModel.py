import numpy as np
import random

class WindModel():
    NONE, N, NE, E, SE, S, SW, W, NW = range(9)
    def __init__(self, n, m, seed):
        self.n = n
        self.m = m
        self.seed = seed
        np.random.seed(self.seed)
        random.seed(self.seed)
        #self.windDirection = random.randrange(0,8)
        self.windDirection = self.N
        self.windSpeed = random.random()
        print("Wind direction: ", self.windDirection)
        print("Wind speed: ", self.windSpeed*30, "m/s")
        print("Normalized Wind speed: ", self.windSpeed)

    def get_direction(self, i,j):
        if i < 0 and j == 0:
            return self.S
        elif i < 0 and j > 0:
            return self.SW
        elif i == 0 and j > 0:
            return self.W
        elif i > 0 and j > 0:
            return self.NW
        elif i > 0 and j == 0:
            return self.N
        elif i > 0 and j < 0:
            return self.NE
        elif i == 0 and j < 0:
            return self.E
        elif i < 0 and j < 0:
            return self.SE
        else:
            return self.NONE

    def get_wind_coefficient(self, x, y):
        if self.windDirection != self.NONE and self.windDirection == self.get_direction(x,y):
            return self.windSpeed
        else:
            return 1