from Model import CombustionModel
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors
import numpy as np

model = CombustionModel(64, 64, 1, False)
colors_list_fire = ['black', (0, 0, 0, 0), 'brown', 'orangered']
model = CombustionModel(64,64,1, False)
colors_list_spread = ['blue', 'green', 'darkgreen', 'brown']
cmap_fire = colors.ListedColormap(colors_list_fire)
cmap_spread = colors.ListedColormap(colors_list_spread)
bounds_fire = [-1, 0, 1, 2]
bounds_spread = [0, 1, 2, 3, 4]
norm_fire = colors.BoundaryNorm(bounds_fire, cmap_fire.N)
norm_spread = colors.BoundaryNorm(bounds_spread, cmap_spread.N)

fig = plt.figure(figsize=(25 / 3, 6.25))
ax = fig.add_subplot(111)
ax.set_axis_off()
ax.imshow(model.EcoModel.terrainMap, cmap=cmap_spread, norm=norm_spread)
im = ax.imshow(model.FireModel.fireMap, cmap=cmap_fire, norm=norm_fire)  # , interpolation='nearest')


# The animation function: called to produce a frame for each generation.
def animate(i):
    im.set_data(animate.X)
    model.spread()
    animate.X = model.FireModel.fireMap


# Bind our grid to the identifier X in the animate function's namespace.
animate.X = model.FireModel.fireMap

# Interval between frames (ms).
interval = 500
model.FireModel.start_fire(int(model.n / 2), int(model.m / 2))
anim = animation.FuncAnimation(fig, animate, interval=interval, frames=300)
# anim.save("forest_fire.mp4")
plt.show()
