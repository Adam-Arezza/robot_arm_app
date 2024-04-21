import ttkbootstrap as ttkb
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkbootstrap.constants import GROOVE
from ttkbootstrap import BooleanVar, StringVar
from src.views.slider_controls_view import SliderControls
from src.views.components.joint_readouts import ReadoutsFrame
from typing import Callable


class RobotView(ttkb.Frame):
    def __init__(self, root, parent):
        super().__init__(parent)
        self.root = root
        self.name = 'robot_view'
        self.header = ttkb.Label(self, text='Robot Viewer', font=('default', 12, 'bold'))
        self.configure(padding=(0,0))
        self.slider_controls = None
        self.readouts_frame = None
        self.mode_value = BooleanVar(value=False)
        self.mode_string = StringVar(value='Offline')
        self.check_btn_frame = ttkb.Frame(self, style='default')
        self.toggle_label = ttkb.Label(self.check_btn_frame, 
                                       textvariable=self.mode_string, 
                                       bootstyle='default')

        self.toggle_mode_switch = ttkb.Checkbutton(self.check_btn_frame,
                                                   onvalue=True,
                                                   offvalue=False,
                                                   variable=self.mode_value,
                                                   bootstyle='default')

        self.reset_btn = ttkb.Button(self, 
                                     text="Reset",
                                     style='primary.Outline.TButton')


        #plot setup
        self.fig, self.ax = plt.subplots(subplot_kw=dict(projection="3d"))
        self.fig.figure.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0)
        self.fig.figure.set_figwidth(6)
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
        # Find the maximum range among the three axes
        max_range = max(x_range, y_range, z_range)
        # Set the limits of all three axes to be the same
        self.ax.set_xlim3d([x_limits[0], x_limits[0] + 0.4])
        self.ax.set_ylim3d([y_limits[0], y_limits[0] + 0.4])
        self.ax.set_zlim3d([z_limits[0], z_limits[0] + 0.4])


        #place widgets
        self.header.pack(pady=10, padx=10)
        self.canvas_plot = FigureCanvasTkAgg(self.fig, self)
        self.canvas_plot.get_tk_widget().pack(anchor='ne', side='right', padx=(0,20), pady=0)
        self.toggle_label.pack()
        self.toggle_mode_switch.pack(padx=10, pady=5)
        self.check_btn_frame.pack()
        self.reset_btn.pack()
        self.robot_plot = None
        self.sim_plot = None


    def draw_robot(self, joint_coords:list):
        color = 'red'
        markerfacecolor = 'blue'
        markeredgecolor = 'blue'
        #if not in online mode, draw with inverted colors
        if not self.mode_value.get():
            color = 'blue'
            markerfacecolor = 'red'
            markeredgecolor = 'red'
        xs, ys, zs = joint_coords 
        if self.robot_plot:
            self.robot_plot.remove()
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


    def add_controls(self, cb, links:list):
        if self.slider_controls:
            self.slider_controls.destroy()
            self.readouts_frame.destroy()
        self.slider_controls = SliderControls(self, cb, links)
        self.readouts_frame = ReadoutsFrame(self, len(links))
        self.slider_controls.pack(padx=20)
        self.readouts_frame.pack(padx=20,pady=20)


    def close(self):
        self.fig.clf()
        self.ax.cla()
        plt.close()
