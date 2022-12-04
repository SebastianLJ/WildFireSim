from Model import CombustionModel
from Model import Log
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors
import numpy as np

model = CombustionModel(64, 64, 44, False)
prediction_model = CombustionModel(64, 64, 44, True, 0)
log = Log()
timecap = 5*60*60

colors_list_fire = [(157/255, 69/255, 49/255), (0, 0, 0, 0), 'brown', (252/255,100/255,0/255)]
colors_list_spread = [(156/255, 212/255, 226/255), (138/255, 181/255, 73/255), (95/255, 126/255, 48/255), (186/255, 140/255, 93/255), (41/255, 150/255, 23/255)]
cmap_fire = colors.ListedColormap(colors_list_fire)
cmap_spread = colors.ListedColormap(colors_list_spread)
bounds_fire = [-1, 0, 1, 2]
bounds_spread = [0, 1, 2, 3, 4, 5]
norm_fire = colors.BoundaryNorm(bounds_fire, cmap_fire.N)
norm_spread = colors.BoundaryNorm(bounds_spread, cmap_spread.N)

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111)
ax.set_axis_off()
ax.imshow(prediction_model.EcoModel.terrainMap, cmap=cmap_spread, norm=norm_spread)
im = ax.imshow(prediction_model.FireModel.fireMap, cmap=cmap_fire, norm=norm_fire)  # , interpolation='nearest')


# The animation function: called to produce a frame for each generation.
def animate(i):
    im.set_data(animate.X)
    model.spread()
    prediction_model.spread(model.spreadMap)
    log.add(model.time, model.FireModel.fireMap, prediction_model.FireModel.fireMap)
    animate.X = prediction_model.FireModel.fireMap
    print(model.time/60/60)
    if(model.FireModel.isFireDone() or model.time >= timecap):
        #log.write(model.seed, model.n, model.m, prediction_model.droneCount)
        im.set_data(animate.X)
        anim.event_source.stop()


# Bind our grid to the identifier X in the animate function's namespace.
animate.X = model.FireModel.fireMap
# Interval between frames (ms). 
interval = 300
model.FireModel.start_fire(int(model.n / 2), int(model.m / 2))
prediction_model.FireModel.start_fire(int(model.n / 2), int(model.m / 2))
log.add(model.time, model.FireModel.fireMap, prediction_model.FireModel.fireMap)
anim = animation.FuncAnimation(fig, animate, interval=interval, frames=300)
# anim.save("forest_fire.mp4")

plt.show()
