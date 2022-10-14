from BaseModel import WilfireModel
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors

model = WilfireModel(100,100,50)

colors_list = [(0.2,0.2,0),'green', 'brown', 'orange']
cmap = colors.ListedColormap(colors_list)
bounds = [-1,0,1,2]
norm = colors.BoundaryNorm(bounds, cmap.N)

fig = plt.figure(figsize=(25/3, 6.25))
ax = fig.add_subplot(111)
ax.set_axis_off()
im = ax.imshow(model.fireMap, cmap=cmap, norm=norm)#, interpolation='nearest')

# The animation function: called to produce a frame for each generation.
def animate(i):
    im.set_data(animate.X)
    model.spread()
    animate.X = model.fireMap
# Bind our grid to the identifier X in the animate function's namespace.
animate.X = model.fireMap

# Interval between frames (ms).
interval = 50
model.fireMap[int(model.n/2)][int(model.m/2)] = 1
anim = animation.FuncAnimation(fig, animate, interval=interval, frames=200)
#anim.save("forest_fire.mp4")
plt.show()