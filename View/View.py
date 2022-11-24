# Lib
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib import use as use_agg
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors

# path
import sys
import os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

# Module
from Model import EcoModel
from Model import CombustionModel
from Model import Log

colors_list_fire = [(157/255, 69/255, 49/255), (0, 0, 0, 0), 'brown', (252/255,100/255,0/255)]
colors_list_spread = [(156/255, 212/255, 226/255), (138/255, 181/255, 73/255), (95/255, 126/255, 48/255), (186/255, 140/255, 93/255), (41/255, 150/255, 23/255)]
cmap_fire = colors.ListedColormap(colors_list_fire)
cmap_spread = colors.ListedColormap(colors_list_spread)
bounds_fire = [-1, 0, 1, 2]
bounds_spread = [0, 1, 2, 3, 4, 5]
norm_fire = colors.BoundaryNorm(bounds_fire, cmap_fire.N)
norm_spread = colors.BoundaryNorm(bounds_spread, cmap_spread.N)

 # Use Tkinter Agg
use_agg('TkAgg')   



# water : #9cd4e2
# grass : #8ab549
# shrub : #5f7e30
# ground : #ba8c5d
# tree : #299617

def create_window():
    AppFont = 'Any 12'
    sg.theme('DarkAmber')
    legend_col = [[sg.Text('Water'),sg.Button(size=(2,1),button_color="#d4f1f9 ")],
                [sg.Text('Grass'),sg.Button(size=(2,1),button_color="#509e02")],
                [sg.Text('Shrub'),sg.Button(size=(2,1),button_color="#7ca814")],
                [sg.Text('Trees'),sg.Button(size=(2,1),button_color="#355426 ")],
                [sg.Text('Ground'),sg.Button(size=(2,1),button_color="#8F653F")],
                
    ]

    left_col = [[sg.Text('Seed'),sg.Input(key='-SEED-'),sg.Button('Generate Bio',key='-GENERATE-',enable_events=True)],
                [sg.Canvas(key='-Graph1-')], 
                [sg.Button('Reset',pad=((2,0),(5,0)),enable_events=True,key='-RESET-'),
                 sg.Button('Save Simulation',pad=((2,0),(5,0)),enable_events=True,key='-SAVE-')]]
    
    right_col = [[sg.Button('Start',button_color='white on green',enable_events=True,key='-START-'), 
                    sg.Button('Stop',button_color='white on red',key='-STOP-'),],
                    [sg.Canvas(key='-Graph2-')],
                    [sg.Button('Exit',pad=((2,0),(5,0)),enable_events=True,key="-EXIT-"),
                ]]
    stat_col = [[sg.Text('Windspeed m/s:'),sg.Text('',key='-WINDSPEED-')],
                [sg.Text('Wind Direction:'),sg.Text('',key='-WINDDIR-')],
                [sg.Text('Time Elapsed:'),sg.Text('',key='-TIME-')],
                [sg.Text('Model Difference:'),sg.Text('',key='-MODELDIFF-')]]

    layout = [[sg.Column(legend_col,element_justification='r'),
               sg.Column(left_col,element_justification='c'),
               sg.VSeperator(),
               sg.Column(right_col,element_justification='c'),
               sg.Column(stat_col,element_justification='l')],
            ]
    created_window = sg.Window('Fire Simulation',
                                layout,
                                finalize=True,
                                resizable=True,
                                icon="fire_logo.ico",
                            )
    return created_window



def color_terrain_map(terrain_map):
        # Water , Grass , Tree , Ground , Shrub
        colors = np.array([[212,241,249], [80, 158, 2], [37, 82, 16], [143, 101, 63], [124, 168, 20]], dtype=np.uint8)
        image = colors[terrain_map.reshape(-1)].reshape(terrain_map.shape+(3,))
        return image

def pack_figure(graph, figure):
    canvas = FigureCanvasTkAgg(figure, graph.Widget)
    plot_widget = canvas.get_tk_widget()
    plot_widget.pack(side='top', fill='both', expand=1)
    
    return plot_widget

def plot_figure(index, image,title):
    fig = plt.figure(index,facecolor=0.7)         # Active an existing figure
    ax = plt.gca()                  # Get the current axes
    ax.cla()                        # Clear the current axes
    ax.set_axis_off()
    ax.set_title(title,loc='center')
    plt.imshow(image)
    fig.tight_layout()
    fig.canvas.draw()    

def clear_plot(index):
    fig = plt.figure(index)
    ax = plt.gca()
    ax.cla()
    ax.set_axis_off()
    fig.canvas.draw() 
    
    
# The animation function: called to produce a frame for each generation.
def animate(i,im,model,prediction_model):
    im.set_data(animate.X)
    model.spread()
    prediction_model.spread(model.spreadMap)
    #log.add(model.time, model.FireModel.fireMap, prediction_model.FireModel.fireMap)
    animate.X = model.FireModel.fireMap
    print(model.time/60/60)
    # if(model.FireModel.isFireDone()):
    #     log.write(model.seed, model.n, model.m, prediction_model.droneCount)
    #     im.set_data(animate.X)
    #     anim.event_source.stop()


if __name__=="__main__":
    n=128
    m=128
    animation_flag=True
    title1="Real World Model"
    title2="Predicted Model"
    # Generate window
    window = create_window()
    # Simulation starting flag
    simulation_start=False
    # Initial graphs
    graph1 = window['-Graph1-']
    graph2 = window['-Graph2-']
    plt.ioff()                                            # Turn the interactive mode off
    fig1 = plt.figure(1,facecolor='white')                # Create a new figure
    ax1 = plt.subplot(111)                                # Add a subplot to the current figure.
    ax1.set_title(title1,loc='center')
    ax1.set_axis_off()
    fig2 = plt.figure(2,facecolor='white')                # Create a new figure
    ax2 = plt.subplot(111)                                # Add a subplot to the current figure.
    ax2.set_title(title2,loc='center')
    ax2.set_axis_off()
    pack_figure(graph1, fig1)                             # Pack figure under graph
    pack_figure(graph2, fig2)
    

     # MAIN LOOP
    while True:
            event, values = window.read(timeout=200)
            if event == sg.WIN_CLOSED or event == '-EXIT-':
                break
            if event == '-GENERATE-':
                if not simulation_start:
                    generated_flag=True
                    selected_seed=int(values['-SEED-'])
                    test_terrain=EcoModel(n=n,m=m,seed=selected_seed)
                    test_terrain.generate_terrain()
                    im=color_terrain_map(test_terrain.terrainMap)
                    plot_figure(1,im, title=title1)
                    plot_figure(2,im, title=title2)
                    
            if event == '-SAVE-':
                print("Saved Simulation to directory: _INSERT_DIRECTORY_")
                # anim.save("forest_fire.mp4")
            if event == '-START-':
                if generated_flag:
                    simulation_start=True
                    model = CombustionModel(128, 128, selected_seed, False)
                    prediction_model = CombustionModel(128, 128, selected_seed, True, 0)
                    log = Log()
                    fig = plt.figure(figsize=(25 / 3, 6.25))
                    ax = fig.add_subplot(111)
                    ax.set_axis_off()
                    fig.tight_layout()
                    fig.canvas.toolbar_visible=False
                    model.seed=selected_seed
                    ax.imshow(test_terrain.terrainMap, cmap=cmap_spread, norm=norm_spread)
                    im = ax.imshow(model.FireModel.fireMap, cmap=cmap_fire, norm=norm_fire)  # , interpolation='nearest')


                    # Bind our grid to the identifier X in the animate function's namespace.
                    animate.X = model.FireModel.fireMap
                    # Interval between frames (ms). 
                    interval = 100
                    model.FireModel.start_fire(int(model.n / 2)-26, int(model.m / 2)+3)
                    prediction_model.FireModel.start_fire(int(model.n / 3), int(model.m / 3))
                    log.add(model.time, model.FireModel.fireMap, prediction_model.FireModel.fireMap)
                    anim = animation.FuncAnimation(fig, animate, interval=interval, frames=300, fargs=(im,model,prediction_model))
                    # anim.save("forest_fire.mp4")

                    fig.show()

                    
                print("Simulation Started")
            if event == '-STOP-':
                simulation_start=False
                print("Simulation Stopped")
            if event == '-RESET-':
                window['-SEED-'].Update('')
                clear_plot(1)
                clear_plot(2)
                simulation_start=False
                generated_flag=False
    
    window.close()
