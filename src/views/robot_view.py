import ttkbootstrap as ttkb
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkbootstrap.constants import GROOVE
from ttkbootstrap import BooleanVar, StringVar
from src.utils import to_degrees, rot_mat_to_euler


class RobotView(ttkb.Frame):
    def __init__(self, root, parent):
        super().__init__(parent)
        self.root = root
        self.name = 'robot_view'
        self.configure(padding=(0,0))
        self.plot_readouts = None
        self.robot_plot = None
        self.ee_axis = []
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
        self.gen_data_btn = ttkb.Button(self, text="Generate Pose Data")
        self.gen_data_btn.pack()
       

    def draw_robot(self, joint_coords:list, rotation_mat:list):
        color = 'red'
        markerfacecolor = 'blue'
        markeredgecolor = 'blue'
        #if not in online mode, draw with inverted colors
        if not self.root.online_mode:
            color = 'blue'
            markerfacecolor = 'red'
            markeredgecolor = 'red'
        xs, ys, zs = joint_coords
        ee_pose = [xs[-1], ys[-1], zs[-1]]       
        euler_angles = rot_mat_to_euler(rotation_mat)
        if self.robot_plot:
            self.robot_plot.remove()
            for quiver in self.ee_axis:
                quiver.remove()
            self.ee_axis.clear()
        if not self.plot_readouts:
            self.draw_readouts()
            self.draw_end_effector_pose([j[-1] for j in joint_coords], euler_angles)
        else:
            joint_angles = to_degrees(self.root.main_container.robot_handler.model.robot.q)
            for i in range(len(joint_angles)):
                self.plot_readouts[i].set_text(f'J{i+1}: {joint_angles[i]}')
            self.ee_pose.remove()
            self.draw_end_effector_pose([j[-1] for j in joint_coords], euler_angles)

        self.robot_plot, = self.ax.plot(xs=xs, 
                                        ys=ys, 
                                        zs=zs,
                                        color=color,
                                        linewidth=3,
                                        marker='o',
                                        markersize=5,
                                        markerfacecolor=markerfacecolor,
                                        markeredgecolor=markeredgecolor)
        qx = self.ax.quiver(ee_pose[0],ee_pose[1],ee_pose[2],rotation_mat[0,0], rotation_mat[1,0], rotation_mat[2,0], color="r", length=0.05, normalize=True)
        qy = self.ax.quiver(ee_pose[0],ee_pose[1],ee_pose[2],rotation_mat[0,1], rotation_mat[1,1], rotation_mat[2,1], color="g", length=0.05, normalize=True)
        qz = self.ax.quiver(ee_pose[0],ee_pose[1],ee_pose[2],rotation_mat[0,2], rotation_mat[1,2], rotation_mat[2,2], color="b", length=0.05, normalize=True)
        self.ee_axis.append(qx)
        self.ee_axis.append(qy)
        self.ee_axis.append(qz)
        self.canvas_plot.draw()
        self.canvas_plot.flush_events()


    def draw_readouts(self):
        self.plot_readouts = []
        x_coord = 0.025
        y_coord = 0.9
        joint_angles = to_degrees(self.root.main_container.robot_handler.model.robot.q)
        for i in range(len(joint_angles)):
            joint_readout = self.fig.text(x=x_coord,
                                          y=y_coord,
                                          s=f'J{i+1}: {joint_angles[i]}',
                                          color='lime',
                                          fontsize='x-large')
            self.plot_readouts.append(joint_readout)
            y_coord -= 0.03


    def draw_end_effector_pose(self, pose, angles):
        linear = ["x", "y", "z"]
        angular = ["r", "p", "y"]
        pose_text = [linear[i]+":"+str(round(pose[i],3))+" "  for i in range(len(linear))]
        angle_text = [angular[i]+":"+str(round(angles[i],2))+" " for i in range(len(angular))]
        ee_text = pose_text + angle_text
        ee_text = "".join(ee_text)
        self.ee_pose = None
        x = 0.025
        y = 0.96
        #ee_frame = axis drawn on the end effector point representing its orientation
        self.ee_pose = self.fig.text(x=x, y=y, s=f'End Effector: {ee_text}',color='lime',fontsize='x-large')
        

    def draw_square(self, square_points):
        pass


    def draw_circle(self, circle_points):
        pass

    def close(self):
        self.fig.clf()
        self.ax.cla()
        plt.close()
