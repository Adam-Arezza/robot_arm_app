import ttkbootstrap as ttkb
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkbootstrap.constants import GROOVE
from ttkbootstrap import BooleanVar, StringVar
#from src.views.slider_controls_view import SliderControls
from src.utils import to_degrees


class RobotView(ttkb.Frame):
    def __init__(self, root, parent):
        super().__init__(parent)
        self.root = root
        self.name = 'robot_view'
        self.configure(padding=(0,0))
        self.plot_readouts = None
        self.robot_plot = None
        self.fig, self.ax = plt.subplots(subplot_kw=dict(projection="3d"))
        self.fig.figure.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0)
        self.fig.figure.set_figwidth(8)
        self.fig.figure.set_facecolor('black')
        self.ax.set_facecolor('black')
        self.ax.set_box_aspect([1,1,1])
        self.ax.autoscale(enable=True, axis="both", tight=False)
        x_limits = self.ax.get_xlim3d()
        y_limits = self.ax.get_ylim3d()
        z_limits = self.ax.get_zlim3d()
        x_range = abs(x_limits[1] - x_limits[0])
        y_range = abs(y_limits[1] - y_limits[0])
        z_range = abs(z_limits[1] - z_limits[0])
        max_range = max(x_range, y_range, z_range)
        self.ax.set_xlim3d([x_limits[0], x_limits[0] + 0.4])
        self.ax.set_ylim3d([y_limits[0], y_limits[0] + 0.4])
        self.ax.set_zlim3d([z_limits[0], z_limits[0] + 0.4])
        self.canvas_plot = FigureCanvasTkAgg(self.fig, self)
        self.canvas_plot.get_tk_widget().pack(anchor='ne', side='right', padx=(0,20), pady=0)
       

    def draw_robot(self, joint_coords:list):
        color = 'red'
        markerfacecolor = 'blue'
        markeredgecolor = 'blue'
        #if not in online mode, draw with inverted colors
        if not self.root.online_mode:
            color = 'blue'
            markerfacecolor = 'red'
            markeredgecolor = 'red'
        xs, ys, zs = joint_coords 
        if self.robot_plot:
            self.robot_plot.remove()
        if not self.plot_readouts:
            self.draw_readouts()
        else:
            joint_angles = to_degrees(self.root.main_container.robot_controller.model.robot.q)
            for i in range(len(joint_angles)):
                self.plot_readouts[i].set_text(f'J{i+1}: {joint_angles[i]}')

        self.robot_plot, = self.ax.plot(xs=xs, 
                                        ys=ys, 
                                        zs=zs,
                                        color=color,
                                        linewidth=3,
                                        marker='o',
                                        markersize=5,
                                        markerfacecolor=markerfacecolor,
                                        markeredgecolor=markeredgecolor)
        self.canvas_plot.draw()
        self.canvas_plot.flush_events()


    def draw_readouts(self):
        self.plot_readouts = []
        x_coord = 0.025
        y_coord = 0.9
        joint_angles = to_degrees(self.root.main_container.robot_controller.model.robot.q)
        for i in range(len(joint_angles)):
            joint_readout = self.fig.text(x=x_coord,
                                          y=y_coord,
                                          s=f'J{i+1}: {joint_angles[i]}',
                                          color='lime',
                                          fontsize='x-large')
            self.plot_readouts.append(joint_readout)
            y_coord -= 0.03


    def close(self):
        self.fig.clf()
        self.ax.cla()
        plt.close()
