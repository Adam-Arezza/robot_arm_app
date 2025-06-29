import ttkbootstrap as ttkb
from ttkbootstrap.constants import GROOVE

class JointController(ttkb.Frame):
    def __init__(self, parent, joint_name, cb, joint_range, default_value, joint_idx, increment):
        super().__init__(parent)
        #self.configure(borderwidth=1, relief=GROOVE)
        self.joint_value = ttkb.IntVar()
        self.joint_value.set(default_value)
        self.increment = increment
        self.joint_range = joint_range
        label = ttkb.Label(self, text=joint_name.replace("_", " ").capitalize(), font=('Helvetica', 10, 'bold'))
        self.joint_idx = joint_idx
        self.increase_angle_btn = ttkb.Button(text=">", command=self.increase_joint_angle)
        self.decrease_angle_btn = ttkb.Button(text="<", command=self.decrease_joint_angle)
        self.increase_speed_btn = ttkb.Button(text="+", command=self.increase_speed)
        self.decrease_speed_btn = ttkb.Button(text="-", command=self.decrease_speed)
        value = ttkb.Label(parent, textvariable=self.joint_value, font=('Helvetica', 12, 'bold'))
        self.increase_angle_btn.pack()
        self.decrease_angle_btn.pack()
        self.increase_speed_btn.pack()
        self.decrease_speed_btn.pack()
        label.pack()
        value.pack()
        self.cb = cb

    def set_joint_value(self, s:int):
        self.joint_value.set(s)
        self.cb(self.joint_idx)

    def increase_joint_angle(self):
        current_value = self.joint_value.get()
        new_value = current_value + self.increment
        if new_value > self.joint_range[1]:
            return
        else:
            self.joint_value.set(current_value + self.increment)

    def decrease_joint_angle(self):
        current_value = self.joint_value.get()
        new_value = current_value - self.increment
        if new_value < self.joint_range[1]:
            return
        else:
            self.joint_value.set(current_value + self.increment)

    def increase_speed(self):
        pass
    def decrease_speed(self):
        pass

