# Lib
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib import use as use_agg
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors
import threading
import time
import matplotlib as mpl
mpl.rcParams['toolbar'] = 'None'

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
colors_list_spread = [(156/255, 212/255, 226/255), (80/255, 158/255, 2/255), (37/255, 82/255, 16/255), (143/255, 101/255, 63/255), (124/255, 168/255, 20/255)]
#colors_list_spread = [(156/255, 212/255, 226/255), (138/255, 181/255, 73/255), (95/255, 126/255, 48/255), (186/255, 140/255, 93/255), (41/255, 150/255, 23/255)]
color_list_drone = [(0,0,0,0),'blue', 'blue', 'blue', (245/255, 245/255, 245/255, 1)]
cmap_fire = colors.ListedColormap(colors_list_fire)
cmap_spread = colors.ListedColormap(colors_list_spread)
cmap_drone = colors.ListedColormap(color_list_drone)
bounds_fire = [-1, 0, 1, 2]
bounds_spread = [0, 1, 2, 3, 4, 5]
bounds_drone = [0, 1, 2,3,4,5]
norm_fire = colors.BoundaryNorm(bounds_fire, cmap_fire.N)
norm_spread = colors.BoundaryNorm(bounds_spread, cmap_spread.N)
norm_drone = colors.BoundaryNorm(bounds_drone, cmap_drone.N)
 # Use Tkinter Agg
use_agg('TkAgg')   

def create_window():
    AppFont = 'Any 12'
    sg.theme('DarkAmber')
    legend_col = [[sg.Text('Water'),sg.Button(size=(2,1),button_color="#9cd4e2")],
                [sg.Text('Grass'),sg.Button(size=(2,1),button_color="#509e02")],
                [sg.Text('Shrub'),sg.Button(size=(2,1),button_color="#7ca814")],
                [sg.Text('Trees'),sg.Button(size=(2,1),button_color="#355426 ")],
                [sg.Text('Ground'),sg.Button(size=(2,1),button_color="#8f6542")],
    ]

    #left_col = [[sg.Text('Seed'),sg.Input(key='-SEED-'),sg.Button('Generate Bio',key='-GENERATE-',enable_events=True)],
    #            [sg.Canvas(key='-Graph1-')], 
    #           [sg.Button('Reset',pad=((2,0),(5,0)),enable_events=True,key='-RESET-'),
    #             sg.Button('Save Simulation',pad=((2,0),(5,0)),enable_events=True,key='-SAVE-')]]
    
    left_col2 = [[sg.Text('Seed'),sg.Input(key='-SEED-',default_text="0"),sg.Button('Generate Bio',key='-GENERATE-',enable_events=True)],
            [sg.Canvas(key='-Graph1-')], 
            [sg.Button('Reset',pad=((2,0),(5,0)),enable_events=True,key='-RESET-'),
                sg.Button('Save Simulation',pad=((2,0),(5,0)),enable_events=True,key='-SAVE-'),
                sg.Button('Start',pad=((2,0),(5,0)),button_color='white on green',enable_events=True,key='-START-'), 
                sg.Button('Stop',pad=((2,0),(5,0)),button_color='white on red',key='-STOP-'),
                sg.Button('Exit',pad=((2,0),(5,0)),enable_events=True,key="-EXIT-")],   
                ]


    right_col = [[sg.Button('Start',button_color='white on green',enable_events=True,key='-START-'), 
                    sg.Button('Stop',button_color='white on red',key='-STOP-'),],
                    [sg.Canvas(key='-Graph2-')],
                    [sg.Button('Exit',pad=((2,0),(5,0)),enable_events=True,key="-EXIT-"),
                ]] 
    stat_col = [[sg.Text('Windspeed'),sg.Text('',key='-WINDSPEED-',text_color='black',background_color='white'), sg.Text("m/s")],
                [sg.Text('Time Elapsed:'),sg.Text('',key='-TIME-',text_color='black',background_color='white',),sg.Text('hours')],
                [sg.Text('Number of Drones'),sg.Input(key='-DRONES-',size=(5,2),default_text="0")],
                [sg.Text('Fire start pos'),sg.Input(key='-FIRESTART-',size=(5,3),default_text="0,0")]
                ]

    # layout = [[sg.Column(legend_col,element_justification='r'),
    #          sg.Column(left_col,element_justification='c'),
    #          sg.VSeperator(),
    #          sg.Column(right_col,element_justification='c'),
    #          sg.Column(stat_col,element_justification='l')],
    #       ]#
    layout2 = [[sg.Column(legend_col,element_justification='r'),
               sg.Column(left_col2,element_justification='c'),
               sg.VSeperator(),
               sg.Column(stat_col,element_justification='l')],
            ]
    created_window = sg.Window('Fire Simulation',
                                layout2,
                                finalize=True,
                                resizable=True,
                                icon="fire_logo.ico",
                            )
    return created_window


def color_terrain_map(terrain_map):
        # Water , Grass , Tree , Ground , Shrub
        colors = np.array([[156,212,226], [80, 158, 2], [37, 82, 16], [143, 101, 63], [124, 168, 20]], dtype=np.uint8)
        image = colors[terrain_map.reshape(-1)].reshape(terrain_map.shape+(3,))
        return image

def pack_figure(graph, figure):
    canvas = FigureCanvasTkAgg(figure, graph.Widget)
    plot_widget = canvas.get_tk_widget()
    plot_widget.pack(side='top', fill='both', expand=1)
    
    return plot_widget

def plot_figure(index, image,title,model):
    fig = plt.figure(index,facecolor=0.7)         # Active an existing figure
    ax = plt.gca()                  # Get the current axes
    ax.cla()                        # Clear the current axes
    ax.set_axis_off()
    ax.set_title(title,loc='center')
    plt.imshow(image)
    x,y = np.meshgrid(np.linspace(0,n-1,10),np.linspace(0,m-1,10))
    u =model.WindModel.wind_vector_a
    v =-model.WindModel.wind_vector_b
    plt.quiver(x,y,u,v,pivot="middle",color=(0, 0, 0, 0.2))
    fig.tight_layout()
    fig.canvas.draw()    

def clear_plot(index):
    fig = plt.figure(index)
    ax = plt.gca()
    ax.cla()
    ax.set_axis_off()
    fig.canvas.draw() 
    
    
# The animation function: called to produce a frame for each generation.
def animate(i,im,model,window):
    # animate.X = model.FireModel.fireMap
    im.set_data(model.FireModel.fireMap)
    model.spread()
    # animate.X = model.FireModel.fireMap
    time_elapsed = model.time/60/60
    window["-TIME-"].update(round(time_elapsed,2))
    window["-WINDSPEED-"].update(round(model.WindModel.windSpeed*30,2))
    
    return im
  
def animate2(i,im,dm,model1,pmodel):
    im.set_data(animate.X)
    dm.set_data(animate.Y)
    model1.spread()
    pmodel.spread(model1.spreadMap)
   # log.add(model.time, model.FireModel.fireMap, prediction_model.FireModel.fireMap)
    animate.X = pmodel.FireModel.fireMap
    animate.Y = pmodel.DroneModel.viewMap
    
    return im
   # if(model.FireModel.isFireDone()):
   #     log.write(model.seed, model.n, model.m, prediction_model.droneCount)
   #     im.set_data(animate.X)
        #anim.event_source.stop()


if __name__=="__main__":
    n=64
    m=64
    n_drones=5
    animation_flag=True
    #title1="Real World Model"
    title1="Generated EcoSystem"
    title2="Predicted Model"
    # Generate window
    window = create_window()
    # Simulation starting flag
    simulation_start=False
    # Initial graphs
    graph1 = window['-Graph1-']
    #graph2 = window['-Graph2-']
    plt.ioff()                                            # Turn the interactive mode off
    fig1 = plt.figure(1,facecolor='white')                # Create a new figure
    ax1 = plt.subplot(111)                                # Add a subplot to the current figure.
    ax1.set_title(title1,loc='center')
    ax1.set_axis_off()
    #fig2 = plt.figure(2,facecolor='white')                # Create a new figure
    #ax2 = plt.subplot(111)                                # Add a subplot to the current figure.
    #ax2.set_title(title2,loc='center')
    #ax2.set_axis_off()
    pack_figure(graph1, fig1)                             # Pack figure under graph
    #pack_figure(graph2, fig2)
    

     # MAIN LOOP
    while True:
            event, values = window.read(timeout=200)
            if event == sg.WIN_CLOSED or event == '-EXIT-':
                break
            if event == '-GENERATE-':
                if not simulation_start:
                    generated_flag=True
                    selected_seed=int(values['-SEED-'])
                    model = CombustionModel(n, m, selected_seed, False)
                    model.seed=selected_seed
                    model2 = CombustionModel(n,m, selected_seed, False)
                    model2.seed=selected_seed
                    im=color_terrain_map(model.EcoModel.terrainMap)
                    im2=color_terrain_map(model2.EcoModel.terrainMap)
                    n_drones=int(values['-DRONES-'])
                    f_pos = str(values['-FIRESTART-'])
                    f_start_x, f_start_y = f_pos.split(',')
                    f_start_x=int(f_start_x)
                    f_start_y=int(f_start_y)
                    fig = plt.figure(1,facecolor=0.7)
                    plot_figure(1,im, title=title1,model=model)
                    #plot_figure(2,im, title=title2,model=model)
                    
                  
            if event == '-SAVE-':
                print("Saved Simulation to directory: View/")
                writervideo = animation.FFMpegWriter(fps=60) 
                anim.save("forest_fire.mp4",writer=writervideo)
            if event == '-START-':
                if generated_flag:
                    simulation_start=True
                    n_drones=int(values['-DRONES-'])
                    f_pos = str(values['-FIRESTART-'])
                    f_start_x, f_start_y = f_pos.split(',')
                    f_start_x=int(f_start_x)
                    f_start_y=int(f_start_y)
                    # model = CombustionModel(n, m, selected_seed, False)¨
                    model = CombustionModel(n, m, selected_seed, False)
                    model.seed=selected_seed
                    model2 = CombustionModel(n,m, selected_seed, False)
                    model2.seed=selected_seed
                    im=color_terrain_map(model.EcoModel.terrainMap)
                    im2=color_terrain_map(model2.EcoModel.terrainMap)
                    prediction_model = CombustionModel(n, m, selected_seed, True, n_drones)
                    log = Log()
                    # fig = plt.figure(figsize=(25 / 3, 6.25))
                    fig, (ax1, ax2) = plt.subplots(1, 2)
                    fig.canvas.set_window_title(f"Real World vs Drone Model using {n_drones} drones")
                    
                    # ax = fig.add_subplot(111)
                    fig.set_size_inches(10,5,forward=True)
                    ax1.set_axis_off()
                    ax2.set_axis_off()
                    
                    ax1.axis('off')
                    ax2.axis('off')
                    fig.tight_layout()
                    fig.canvas.toolbar_visible=False

                    ax1.imshow(model.EcoModel.terrainMap, cmap=cmap_spread, norm=norm_spread)
                    ax2.imshow(prediction_model.EcoModel.terrainMap, cmap=cmap_spread, norm=norm_spread)
                    im1 = ax1.imshow(model.FireModel.fireMap, cmap=cmap_fire, norm=norm_fire)  
                    
                    im2 = ax2.imshow(prediction_model.FireModel.fireMap,cmap=cmap_fire, norm=norm_fire)
                    dm = ax2.imshow(prediction_model.DroneModel.viewMap, cmap=cmap_drone, norm=norm_drone, alpha=0.70)  # , interpolation='nearest')

                    x,y = np.meshgrid(np.linspace(0,n-1,10),np.linspace(0,m-1,10))
                    u =model.WindModel.wind_vector_a
                    v =-model.WindModel.wind_vector_b
                    ax1.quiver(x,y,u,v,pivot="middle",color=(0, 0, 0, 0.2))
                    ax2.quiver(x,y,u,v,pivot="middle",color=(0,0,0,0.2))
                    # Bind our grid to the identifier X in the animate function's namespace.
                    animate.X = model2.FireModel.fireMap
                    animate.Y = prediction_model.DroneModel.viewMap
                    # Interval between frames (ms). 
                    interval = 300
                    model.FireModel.start_fire(f_start_x, f_start_y)
                    model2.FireModel.start_fire(f_start_x, f_start_y)
                    prediction_model.FireModel.start_fire(f_start_x, f_start_y)
                    #log.add(model.time, model.FireModel.fireMap, prediction_model.FireModel.fireMap)
                    
                    anim = animation.FuncAnimation(fig, animate, interval=interval, frames=300, fargs=(im1,model,window))
                    anim2 = animation.FuncAnimation(fig,animate2,interval=interval,frames=300, fargs=(im2,dm,model2,prediction_model))
                    # anim2 = animation.FuncAnimation(fig2, animate_drones, interval=interval, frames=300, fargs=(im2,dm2,model,prediction_model))
                    
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
