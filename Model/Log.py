import csv
import numpy as np
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.dirname(__file__))

class Log():
    def __init__(self):
        self.header = ['time', 'fireArea', 'predictedFireArea', 'precision']
        self.log = []

    def add(self, time, fireMap, predictedFireMap):
        fireArea = np.count_nonzero(fireMap)
        predictedFireArea = np.count_nonzero(predictedFireMap)
        # should count true positives and false positives as well as true negatives and false negatives
        precision = (fireArea - (fireArea - predictedFireArea)) / fireArea
        self.log.append([time, fireArea, predictedFireArea, precision])
    
    def write(self, seed, n, m, droneCount):
        filename = 'log_' + str(seed) + '_' + str(n) + '_' + str(m) + '_' + str(droneCount) + '.csv'
        with open("/out/"+filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.header)
            for row in self.log:
                writer.writerow(row)