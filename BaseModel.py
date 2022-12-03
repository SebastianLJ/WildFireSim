import numpy as np
from random import random
import time


class WilfireModel():
    NONE, N, NE, E, SE, S, SW, W, NW = range(9)

    def __init__(self, n, m, seed):
        self.n = n
        self.m = m
        self.seed = seed
        np.random.seed(self.seed)
        random.seed(self.seed)
        self.windDirection = random.randrange(0, 8)
        #print("Wind direction: ", self.windDirection)
        # map of likelyhood of spread represented by a spread coefficient
        self.spreadMap = np.array(np.random.rand(self.n, self.m))
        # map of active fire represented by 0 or 1
        self.fireMap = np.zeros((self.n, self.m), dtype=int)
        np.set_printoptions(threshold=np.inf)

    def startSim(self):
        # init fire
        self.fireMap[int(self.n / 2)][int(self.m / 2)] = 1
        print(self.fireMap)
        while True:
            self.spread()
            print(chr(27) + "[2J")
            print(self.fireMap)
            time.sleep(1)

    def neighbors(self, radius, row_number, column_number):
        # returns matrix containing neighbours
        return [[self.fireMap[i][j] if i >= 0 and i < len(self.fireMap) and j >= 0 and j < len(self.fireMap[0]) else 0
                 for j in range(column_number - 1 - radius, column_number + radius)]
                for i in range(row_number - 1 - radius, row_number + radius)]

    def neighbors_spread(self, radius, row_number, column_number):
        # returns matrix containing neighbours
        return [
            [self.spreadMap[i][j] if i >= 0 and i < len(self.spreadMap) and j >= 0 and j < len(self.spreadMap[0]) else 0
             for j in range(column_number - 1 - radius, column_number + radius)]
            for i in range(row_number - 1 - radius, row_number + radius)]

    def get_direction(self, i, j):
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

    def wind_coefficient(self, x, y):
        if self.windDirection != self.NONE and self.windDirection == self.get_direction(x, y):
            return 5
        else:
            return 1.5

    def get_neighbour_spread_risk(self, neighbors):
        highest_wind = 1
        for i in range(0, len(neighbors)):
            for j in range(0, len(neighbors[i])):
                if neighbors[i][j] == 1:
                    if self.wind_coefficient(i - 1, j - 1) > highest_wind:
                        highest_wind = self.wind_coefficient(i - 1, j - 1)
        return highest_wind

    def spread(self):
        spread = []
        for i, row in enumerate(self.fireMap):
            for j, cell in enumerate(row):
                matrix = np.matrix(self.neighbors(1, i + 1, j + 1))
                if cell == 0 and matrix.sum() > 0:
                    if (self.spreadMap[i][j] * self.get_neighbour_spread_risk(self.neighbors(1, i + 1, j + 1))) >= 1.0:
                        spread.append((i, j))
                elif cell == 1:
                    if self.spreadMap[i][j] < 0.3:
                        self.fireMap[i][j] = -1
                    self.spreadMap[i][j] = self.spreadMap[i][j] * 0.8
        for pair in spread:
            self.fireMap[pair[0]][pair[1]] = 1
