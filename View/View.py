# Lib
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# path
import sys
import os

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

# Module
from Model import EcoModel


class GUI():
    def __init__(self, terrainMap=None):
        self._VARS = {'window': False}
        self.terrainMap = terrainMap

    def layout(self):
        AppFont = 'Any 16'
        sg.theme('DarkAmber')
        
        left_col = [[sg.Text('Seed'),sg.Input(key='-SEED-'),sg.Button('Generate Bio',key='-GENERATE-',enable_events=True)],
                    [sg.Canvas(key='figCanvas')], 
                    [sg.Button('Reset',font=AppFont,pad=((2,0),(5,0)),enable_events=True,key='-RESET-'),
                     sg.Button('Save Simulation',font=AppFont,pad=((2,0),(5,0)),enable_events=True,key='-SAVE-')]]
        
        right_col = [[sg.Button('Start',font=AppFont,pad=((2, 0), (5, 0)),button_color='black on green',enable_events=True,key='-START-'), 
                     sg.Button('Stop',font=AppFont,pad=((2, 0), (5, 0)),button_color='black on red',key='-STOP-'),],
                     [sg.Canvas(key='figCanvas2')],
                     [sg.Button('Exit', font=AppFont,pad=((2,0),(5,0)),enable_events=True,key="-EXIT-"),
                    ]]
        layout = [[sg.Column(left_col,element_justification='c'),sg.VSeperator(),sg.Column(right_col,element_justification='c')],
                ]
        self._VARS['window'] = sg.Window('Fire Simulation',
                                    layout,
                                    finalize=True,
                                    resizable=True,
                                    icon="fire_logo.ico",
                                )
    
    def show(self):
        #
        
        self.fig = plt.figure(facecolor="0.75")
        colors = np.array([[156, 212, 226], [138, 181, 73], [95, 126, 48], [186, 140, 93]], dtype=np.uint8)
        #print(self.terrainMap)
        self.image = colors[self.terrainMap.reshape(-1)].reshape(self.terrainMap.shape+(3,))
        plt.imshow(self.image)
        # Instead of plt.show
        self.draw_figure(self._VARS['window']['figCanvas'].TKCanvas, self.fig)
        
        self.draw_figure(self._VARS['window']['figCanvas2'].TKCanvas, self.fig)
    
    def reset_figure(self):
        self.fig.clf()
        
    def draw_figure(self, canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=0)
        return figure_canvas_agg

    
            
        
if __name__=="__main__":
    #gen
    test_GUI = GUI()
    test_GUI.layout()

    #Simulation starting flag
    simulation_start=False
     # MAIN LOOP
    while True:
            event, values = test_GUI._VARS['window'].read(timeout=200)
            if event == sg.WIN_CLOSED or event == '-EXIT-':
                break
            if event == '-GENERATE-':
                if not simulation_start:
                    
                    selected_seed=int(values['-SEED-'])
                    test_terrain=EcoModel(n=64,m=64,seed=selected_seed)
                    test_terrain.generate_terrain()
                    
                    test_GUI.terrainMap = test_terrain.terrainMap
                    test_GUI.show()
            if event == '-SAVE-':
                print("Saved Simulation to directory: _INSERT_DIRECTORY_")
            if event == '-START-':
                simulation_start=True
                print("Simulation Started")
            if event == '-STOP-':
                simulation_start=False
                print("Simulation Stopped")
            if event == '-RESET-':
                test_GUI._VARS['window'].FindElement('-SEED-').Update('')
                test_GUI.reset_figure()
                
    test_GUI._VARS['window'].close()
