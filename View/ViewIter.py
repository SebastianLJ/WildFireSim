import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors
import numpy as np
# path
import sys
import os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

# Module
from Model import CombustionModel
from Model import Log

n=64
m=64
selected_seed=44
model = CombustionModel(n, m, selected_seed, False)
prediction_model = CombustionModel(n, m, selected_seed, True, 5)
log = Log()
timecap = 0.5*60*60

colors_list_fire = [(157/255, 69/255, 49/255), (0, 0, 0, 0), 'brown', (252/255,100/255,0/255)]
colors_list_spread = [(156/255, 212/255, 226/255), (80/255, 158/255, 2/255), (37/255, 82/255, 16/255), (143/255, 101/255, 63/255), (124/255, 168/255, 20/255)]
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

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111)
ax.set_axis_off()
ax.imshow(prediction_model.EcoModel.terrainMap, cmap=cmap_spread, norm=norm_spread)
dm = ax.imshow(prediction_model.DroneModel.viewMap, cmap=cmap_drone, norm=norm_drone, alpha=0.70)  # , interpolation='nearest')

im = ax.imshow(prediction_model.FireModel.fireMap, cmap=cmap_fire, norm=norm_fire)  # , interpolation='nearest')
x,y = np.meshgrid(np.linspace(0,n-1,10),np.linspace(0,m-1,10))
u =model.WindModel.wind_vector_a
v =-model.WindModel.wind_vector_b
plt.quiver(x,y,u,v,pivot="middle",color=(0, 0, 0, 0.2))

# The animation function: called to produce a frame for each generation.
def animate(i):
    im.set_data(animate.X)
    model.spread()
    prediction_model.spread(model.spreadMap)
    log.add(model.time, model.FireModel.fireMap, prediction_model.FireModel.fireMap)
    animate.X = model.FireModel.fireMap
    print(model.time/60/60)
    if(model.FireModel.isFireDone() or model.time >= timecap):
        #log.write(model.seed, model.n, model.m, prediction_model.droneCount)
        im.set_data(animate.X)
        anim.event_source.stop()

# def animate(i):
#     im.set_data(animate.X)
#     dm.set_data(animate.Y)
#     model.spread()
#     prediction_model.spread(model.spreadMap)
#     log.add(model.time, model.FireModel.fireMap, prediction_model.FireModel.fireMap)
#     animate.X = prediction_model.FireModel.fireMap
#     animate.Y = prediction_model.DroneModel.viewMap
#     #print(model.time/60/60)
#     if(model.FireModel.isFireDone() or model.time >= timecap):
#         #log.write(model.seed, model.n, model.m, prediction_model.droneCount) 
#         im.set_data(animate.X)
#         anim.event_source.stop()

# Bind our grid to the identifier X in the animate function's namespace.
animate.X = model.FireModel.fireMap
animate.Y = prediction_model.DroneModel.viewMap
# Interval between frames (ms). 
interval = 300
# model.FireModel.start_fire(int(model.n / 2)+1, int(model.m / 2))
# prediction_model.FireModel.start_fire(int(model.n / 2)+1, int(model.m / 2))
model.FireModel.start_fire(int(model.n / 2)+30, int(model.m / 2)-19)
prediction_model.FireModel.start_fire(int(model.n / 2)+30, int(model.m / 2)-19)
log.add(model.time, model.FireModel.fireMap, prediction_model.FireModel.fireMap)
anim = animation.FuncAnimation(fig, animate, interval=interval, frames=300)
# anim.save("forest_fire.mp4")

plt.show()
