import csv
import numpy as np
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.dirname(__file__))

class Log():
    def __init__(self):
        self.header = ['time', 'fireArea', 'predictedFireArea', 'accuracy', 'sensitivity', 'specificity', 'tp', 'fp', 'tn', 'fn']
        self.log = []

    def add(self, time, fireMap, predictedFireMap):
        fireArea = np.count_nonzero(fireMap)
        predictedFireArea = np.count_nonzero(predictedFireMap)
        # formulas from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4614595/
        tp = self.get_true_positive(fireMap, predictedFireMap)
        fp = self.get_false_positive(fireMap, predictedFireMap)
        tn = self.get_true_negative(fireMap, predictedFireMap)
        fn = self.get_false_negative(fireMap, predictedFireMap)
        accuracy = (tp + tn) / (tp + fp + tn + fn)
        try:
            sensitivity = tp / (tp + fn)
        except ZeroDivisionError:
            print("Sensitivity error")
            sensitivity = 1.0
        specificity = tn / (tn + fp)
        self.log.append([int(time), fireArea, predictedFireArea, accuracy, sensitivity, specificity, tp, fp, tn, fn])
    
    def write(self, seed, n, m, droneCount, customName = ''):
        filename = 'log_' + str(seed) + '_' + str(n) + '_' + str(m) + '_' + str(droneCount) + customName + '.csv'
        with open("logs/"+filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.header)
            for row in self.log:
                writer.writerow(row)

    def get_true_positive(self, fireMap, predictedFireMap):
        return (np.logical_and(fireMap == 1, predictedFireMap == 1).sum() +
            np.logical_and(fireMap == -1, predictedFireMap == -1).sum())
    
    def get_false_positive(self, fireMap, predictedFireMap):
        return (np.logical_and(np.logical_not(fireMap == 1), predictedFireMap == 1).sum() + 
            np.logical_and(np.logical_not(fireMap == -1), predictedFireMap == -1).sum())

    def get_true_negative(self, fireMap, predictedFireMap):
        return (np.logical_and(np.logical_not(fireMap == 1), np.logical_not(predictedFireMap == 1)).sum() +
            np.logical_and(np.logical_not(fireMap == -1), np.logical_not(predictedFireMap == -1)).sum())

    def get_false_negative(self, fireMap, predictedFireMap):
        return (np.logical_and(fireMap == 1, np.logical_not(predictedFireMap == 1)).sum() +
            np.logical_and(fireMap == -1, np.logical_not(predictedFireMap == -1)).sum())