import ttkbootstrap as ttk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk

class MainCanvas:
    def __init__(self, root):
        self.root = root
        self.canvas = ttk.Canvas(self.root)
        matplotlib.use('TkAgg')
        px = 1/plt.rcParams['figure.dpi']
        self.fig = plt.figure(figsize=(1000*px, 800*px))
        self.ax = self.fig.add_subplot(projection='3d')
        self.visual = FigureCanvasTkAgg(self.fig, master=self.root)
        self.visual.draw()
        self.visual.get_tk_widget().pack(side='bottom', pady=20)