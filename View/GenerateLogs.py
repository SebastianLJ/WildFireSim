from Model import CombustionModel
from Model import Log
import numpy as np

seed = 22
n = 32
m = 32
droneCount = 0

log = Log()

true_model = CombustionModel(n, m, seed, False)
prediction_model = CombustionModel(n, m, seed, True, droneCount)

true_model.FireModel.start_fire(int(n / 2)+3, int(m / 2)+3)
prediction_model.FireModel.start_fire(int(n / 2)+3, int(m / 2)+3)

while(not true_model.FireModel.isFireDone()):
    true_model.spread()
    prediction_model.spread(true_model.spreadMap)
    log.add(true_model.time, true_model.FireModel.fireMap, prediction_model.FireModel.fireMap)

log.write(seed, n, m, droneCount)