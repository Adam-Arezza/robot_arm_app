import ttkbootstrap as ttkb
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkbootstrap.constants import GROOVE


class RobotView(ttkb.Frame):
    def __init__(self, root, parent):
        super().__init__(parent, borderwidth=2, relief=GROOVE)
        self.configure(padding=(0,0))
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
        self.canvas_plot = FigureCanvasTkAgg(self.fig, self)
        self.canvas_plot.get_tk_widget().pack(padx=0, pady=0)
        self.robot_plot = None


    def draw_robot(self, angles, robot):
        #given joint angles, compute the 

        prev_transform = None
        joint_coordinates = [[0],[0],[0]]
        for i in range(len(angles)):
            t_matrix = robot.links[i].A(robot.q[i])  
            t_matrix = np.array(t_matrix)
            new_transform = t_matrix
            if i > 0:
                new_transform = np.dot(prev_transform, t_matrix)
            prev_transform = new_transform
            j_coords = new_transform[:3,3]
            joint_coordinates[0].append(j_coords[0])
            joint_coordinates[1].append(j_coords[1])
            joint_coordinates[2].append(j_coords[2])

        if self.robot_plot:
            self.robot_plot.remove()
        # provide the joint coordinates to ax.plot for each joint
        self.robot_plot, = self.ax.plot(xs=joint_coordinates[0], 
                     ys=joint_coordinates[1], 
                     zs=joint_coordinates[2],
                     color='red',
                     linewidth=3,
                     marker='o',
                     markersize=5,
                     markerfacecolor='blue',
                     markeredgecolor='blue')

        self.canvas_plot.draw()
       # # Plot links as lines between joint positions


    def close(self):
        plt.close()
        self.fig.clf()
        self.ax.cla()

