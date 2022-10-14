import numpy as np
import random
import time

class WilfireModel():
    def __init__(self, n, m, seed):
        self.n = n
        self.m = m
        self.seed = seed
        np.random.seed(self.seed)
        random.seed(self.seed)
        # map of likelyhood of spread represented by a spread coefficient
        self.spreadMap = np.array(np.random.rand(self.n, self.m))
        # map of active fire represented by 0 or 1
        self.fireMap = np.zeros((self.n,self.m), dtype=int)
        np.set_printoptions(threshold=np.inf)

    def startSim(self):
        #init fire
        self.fireMap[int(self.n/2)][int(self.m/2)] = 1
        print(self.fireMap)
        while True:
            self.spread()
            print(chr(27) + "[2J")
            print(self.fireMap)
            time.sleep(1)

    def neighbors(self, radius, row_number, column_number):
        # returns matrix containing neighbours
        return [[self.fireMap[i][j] if  i >= 0 and i < len(self.fireMap) and j >= 0 and j < len(self.fireMap[0]) else 0
            for j in range(column_number-1-radius, column_number+radius)]
                for i in range(row_number-1-radius, row_number+radius)]

    def spread(self):
        spread = []
        for i, row in enumerate(self.fireMap):
            for j, cell in enumerate(row):
                matrix = np.matrix(self.neighbors( 1, i+1, j+1))
                if cell == 0 and matrix.sum() > 0:
                    if random.random() + self.spreadMap[i][j] > 1.0:
                        spread.append((i,j))
        for pair in spread:
            self.fireMap[pair[0]][pair[1]] = 1