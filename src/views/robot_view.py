import ttkbootstrap as ttkb
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class RobotView(ttkb.Frame):
    def __init__(self, root, parent):
        super().__init__(parent)
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
        self.canvas_plot = FigureCanvasTkAgg(self.fig, self)
        self.canvas_plot.get_tk_widget().pack()


    def close(self):
        plt.close()
        self.fig.clf()
        self.ax.cla()

