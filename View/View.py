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
    def __init__(self, terrainMap):
        self._VARS = {'window': False}
        self.terrainMap = terrainMap

    def layout(self):
        AppFont = 'Any 16'
        sg.theme('DarkAmber')

        layout = [[sg.Canvas(key='figCanvas')],
                [sg.Button('Start',
                     font=AppFont,
                     pad=((4, 0), (10, 0))),
                sg.Button('Stop',
                     font=AppFont,
                     pad=((4, 0), (10, 0))),
                sg.Button('Tick Drone Model',
                     font=AppFont,
                     pad=((4, 0), (10, 0))),
                sg.Button('Reset',
                     font=AppFont,
                     pad=((4, 0), (10, 0)))],
                [sg.Button('Exit', font=AppFont)]]
        self._VARS['window'] = sg.Window('Fire Simulation',
                                    layout,
                                    finalize=True,
                                    resizable=True,
                                    element_justification="right")
    
    def show(self):
        #

        self.fig = plt.figure()
        colors = np.array([[156, 212, 226], [138, 181, 73], [95, 126, 48], [186, 140, 93]], dtype=np.uint8)
        #print(self.terrainMap)
        self.image = colors[self.terrainMap.reshape(-1)].reshape(self.terrainMap.shape+(3,))
        plt.imshow(self.image)
        # Instead of plt.show
        self.draw_figure(self._VARS['window']['figCanvas'].TKCanvas, self.fig)
        
        # MAIN LOOP
        while True:
            event, values = self._VARS['window'].read(timeout=200)
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
        self._VARS['window'].close()
        
    def draw_figure(self, canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg
            
        
if __name__=="__main__":
    #gen
    test_terrain=EcoModel(n=64,m=64,seed=2)
    test_terrain.generate_terrain()

    #GUI
    test_GUI = GUI(test_terrain.terrainMap)
    test_GUI.layout()
    test_GUI.show()
