from cProfile import label
from matplotlib import test
import numpy as np
import random
import numpy as np
import matplotlib.pyplot as plt

def generate_perlin_noise_2d(shape, res):
    def f(t):
        return 6*t**5 - 15*t**4 + 10*t**3
    
    delta = (res[0] / shape[0], res[1] / shape[1])
    d = (shape[0] // res[0], shape[1] // res[1])
    grid = np.mgrid[0:res[0]:delta[0],0:res[1]:delta[1]].transpose(1, 2, 0) % 1
    # Gradients
    angles = 2*np.pi*np.random.rand(res[0]+1, res[1]+1)
    gradients = np.dstack((np.cos(angles), np.sin(angles)))
    g00 = gradients[0:-1,0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g10 = gradients[1:,0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g01 = gradients[0:-1,1:].repeat(d[0], 0).repeat(d[1], 1)
    g11 = gradients[1:,1:].repeat(d[0], 0).repeat(d[1], 1)
    # Ramps
    n00 = np.sum(grid * g00, 2)
    n10 = np.sum(np.dstack((grid[:,:,0]-1, grid[:,:,1])) * g10, 2)
    n01 = np.sum(np.dstack((grid[:,:,0], grid[:,:,1]-1)) * g01, 2)
    n11 = np.sum(np.dstack((grid[:,:,0]-1, grid[:,:,1]-1)) * g11, 2)
    # Interpolation
    t = f(grid)
    n0 = n00*(1-t[:,:,0]) + t[:,:,0]*n10
    n1 = n01*(1-t[:,:,0]) + t[:,:,0]*n11
    return np.sqrt(2)*((1-t[:,:,1])*n0 + t[:,:,1]*n1)
        
def generate_fractal_noise_2d(shape, res, octaves=1, persistence=0.5):
    noise = np.zeros(shape)
    frequency = 1
    amplitude = 1
    for _ in range(octaves):
        noise += amplitude * generate_perlin_noise_2d(shape, (frequency*res[0], frequency*res[1]))
        frequency *= 2
        amplitude *= persistence
    return noise

class EcoModel():
    WATER, GRASS, TREE, BARE_GROUND, SHRUB= 0, 1, 2, 3, 4
    def __init__(self, n, m, seed):
        self.n = n
        self.m = m
        self.seed = seed
        self.water_thresh=0.2
        self.tree_thresh=0.1
        self.shrub_thresh=0.15
        np.random.seed(self.seed)
        random.seed(self.seed)
        # Generation of random map
        self.terrainMap = np.ones((self.n,self.m),dtype=np.int32)
        self.elevationMap = np.zeros((self.n,self.m), dtype=int)
        self.nonBurnMap = np.zeros((self.n,self.m), dtype=int)

    def generate_terrain(self):
        self.generate_noise()
        self.add_trees(tree_threshold=self.tree_thresh)
        self.add_shrub(shrub_threshold=self.shrub_thresh)
        self.add_ground()
        self.add_water(water_threshold=self.water_thresh)
        self.add_shrub(self.shrub_thresh)

    def generate_noise(self):
        noise = generate_fractal_noise_2d((self.n,self.m),(1,1),6)
        noise = (noise-noise.min())/(noise.max()-noise.min())
        self.noise_map=noise
    
    def add_water(self,water_threshold):
        self.terrainMap[self.noise_map<water_threshold]=self.WATER
    
    def add_trees(self,tree_threshold):
        potential_tree=((self.noise_map-tree_threshold)/(1-tree_threshold))**2
        tree_mask = (self.noise_map > tree_threshold)*(np.random.rand(self.n,self.m)<potential_tree)
        self.terrainMap[tree_mask]=self.TREE
    
    def add_ground(self):
        ground_mask=(self.terrainMap==1)*(np.random.rand(self.n,self.m)<0.1)
        self.terrainMap[ground_mask]=self.BARE_GROUND

    def add_shrub(self, shrub_threshold):
        potential_shrub=((self.noise_map-shrub_threshold)/(1-shrub_threshold))**2*0.3
        shrub_mask = (self.noise_map > shrub_threshold)*(np.random.rand(self.n,self.m)<potential_shrub)
        self.terrainMap[shrub_mask]=self.SHRUB

    def plot_terrain(self):
        plt.figure()
        colors = np.array([[156, 212, 226], [138, 181, 73], [95, 126, 48], [186, 140, 93], [41, 150, 23]], dtype=np.uint8)
        print(self.terrainMap)
        self.image = colors[self.terrainMap.reshape(-1)].reshape(self.terrainMap.shape+(3,))
        plt.imshow(self.image)

    
    
    def get_spread_rate(self, i, j):
        terrain_type = self.terrainMap[i][j]
        if terrain_type == self.WATER:
            return 0
        elif terrain_type == self.GRASS:
            return 1
        elif terrain_type == self.TREE:
            return 0.6405
        elif terrain_type == self.BARE_GROUND:
            return 0
        elif terrain_type == self.SHRUB:
            return 0.0177

    def get_burn_rate(self, i, j):
        terrain_type = self.terrainMap[i][j]
        if terrain_type == self.WATER:
            return 0
        elif terrain_type == self.GRASS:
            return 10
        elif terrain_type == self.TREE:
            return 3
        elif terrain_type == self.BARE_GROUND:
            return 0
        elif terrain_type == self.SHRUB:
            return 1

if __name__=="__main__":
    test_terrain=EcoModel(n=64,m=64,seed=4)
    test_terrain.generate_terrain()
    test_terrain.plot_terrain()

    test_terrain2=EcoModel(n=64,m=64,seed=5)
    test_terrain2.generate_terrain()
    test_terrain2.plot_terrain()

    plt.show()
