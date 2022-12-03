from Model import CombustionModel
from Model import Log
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors
import numpy as np

model = CombustionModel(128, 128, 120, False)
prediction_model = CombustionModel(128, 128, 120, True, 4)

log = Log()

colors_list_fire = [(157/255, 69/255, 49/255), (0, 0, 0, 0), 'brown', (252/255,100/255,0/255)]
colors_list_spread = [(156/255, 212/255, 226/255), (138/255, 181/255, 73/255), (95/255, 126/255, 48/255), (186/255, 140/255, 93/255), (41/255, 150/255, 23/255)]
color_list_drone = [(0,0,0,0),'blue', 'blue', 'blue', (245/255, 245/255, 245/255, 1)]
cmap_fire = colors.ListedColormap(colors_list_fire)
cmap_spread = colors.ListedColormap(colors_list_spread)
cmap_drone = colors.ListedColormap(color_list_drone)
bounds_fire = [-1, 0, 1, 2]
bounds_spread = [0, 1, 2, 3, 4, 5]
bounds_drone = [0, 1, 2, 3, 4, 5]
norm_fire = colors.BoundaryNorm(bounds_fire, cmap_fire.N)
norm_spread = colors.BoundaryNorm(bounds_spread, cmap_spread.N)
norm_drone = colors.BoundaryNorm(bounds_drone, cmap_drone.N)

fig = plt.figure(figsize=(25 / 3, 6.25))
ax = fig.add_subplot(111)
ax.set_axis_off()
ax.imshow(model.EcoModel.terrainMap, cmap=cmap_spread, norm=norm_spread)
im = ax.imshow(model.FireModel.fireMap, cmap=cmap_fire, norm=norm_fire)
dm = ax.imshow(prediction_model.DroneModel.viewMap, cmap=cmap_drone, norm=norm_drone, alpha=0.70)  # , interpolation='nearest')

# The animation function: called to produce a frame for each generation.
def animate(i):
    im.set_data(animate.X)
    dm.set_data(animate.Y)
    model.spread()
    prediction_model.spread(model.spreadMap)
    log.add(model.time, model.FireModel.fireMap, prediction_model.FireModel.fireMap)
    animate.X = model.FireModel.fireMap
    animate.Y = prediction_model.DroneModel.viewMap
    #print(model.time/60/60)
    if(model.FireModel.isFireDone()):
        log.write(model.seed, model.n, model.m, prediction_model.droneCount)
        im.set_data(animate.X)
        anim.event_source.stop()


# Bind our grid to the identifier X in the animate function's namespace.
animate.X = model.FireModel.fireMap
animate.Y = prediction_model.DroneModel.viewMap
# Interval between frames (ms). 
interval = 1
model.FireModel.start_fire(int(model.n / 2)+3, int(model.m / 2)+3)
prediction_model.FireModel.start_fire(int(model.n / 2)+3, int(model.m / 2)+3)
log.add(model.time, model.FireModel.fireMap, prediction_model.FireModel.fireMap)
anim = animation.FuncAnimation(fig, animate, interval=interval, frames=300)
# anim.save("forest_fire.mp4")

plt.show()