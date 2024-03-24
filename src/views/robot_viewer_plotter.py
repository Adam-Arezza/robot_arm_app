import ttkbootstrap as ttkb
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
        self.timer = plt.figtext(0.85, 0.95, "")
        self.embed_plot()

    def embed_plot(self):
        self.fig, self.ax = plt.subplots(subplot_kw=dict(projection="3d"))
        self.ax.set_box_aspect([1,1,1])
        self.ax.autoscale(enable=True, axis="both", tight=False)
        x_limits = self.ax.get_xlim3d()
        y_limits = self.ax.get_ylim3d()
        z_limits = self.ax.get_zlim3d()

        x_range = abs(x_limits[1] - x_limits[0])
        y_range = abs(y_limits[1] - y_limits[0])
        z_range = abs(z_limits[1] - z_limits[0])

        # Find the maximum range among the three axes
        max_range = max(x_range, y_range, z_range)

        # Set the limits of all three axes to be the same
        self.ax.set_xlim3d([x_limits[0], x_limits[0] + 0.4])
        self.ax.set_ylim3d([y_limits[0], y_limits[0] + 0.4])
        self.ax.set_zlim3d([z_limits[0], z_limits[0] + 0.4])
        self.canvas_plot = FigureCanvasTkAgg(self.fig, self.frame)
        self.canvas_plot.get_tk_widget().pack(side='left')
        #self.add(self.robot)

    def step_plot(self, dt=0.5):
        super().step(dt)
        self.canvas_plot.draw()
    
    def launch(self, name, fig=None, limits=None, **kwargs):
        super().launch(name="testing", fig=self.fig, limits=self.limits)
