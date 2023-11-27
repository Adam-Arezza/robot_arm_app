import ttkbootstrap as ttk
import roboticstoolbox.backends.PyPlot as plotter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class RobotView(plotter.PyPlot):
    def __init__(self, parent, frame, robot):
        super().__init__()
        self.tk_root = parent
        self.robot = robot
        self.parent = parent
        self.frame = frame
        self.limits = [(-1,1),(-1,1),(-1,1)]
        self.sim_time = 0
        self.embed_plot()

    def embed_plot(self):
        self.fig, self.ax = plt.subplots(subplot_kw=dict(projection="3d"))
        self.ax.set_box_aspect([1,1,1])
        self.canvas_plot = FigureCanvasTkAgg(self.fig, self.frame)
        self.canvas_plot.get_tk_widget().pack(side='left')
        self.add(self.robot)

    def step_plot(self, dt=0.5):
        super().step(dt)
        self.canvas_plot.draw()
    
    def launch(self, name, fig=None, limits=None, **kwargs):
        super().launch(fig=self.fig, limits=self.limits)
