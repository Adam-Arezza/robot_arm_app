import ttkbootstrap as ttkb

class JointController(ttkb.Frame):
    def __init__(self, parent, joint_name, cb, joint_range, default_value, joint_idx, getIncrement):
        super().__init__(parent)
        self.joint_value = ttkb.IntVar()
        self.joint_value.set(default_value)
        self.joint_range = joint_range
        label = ttkb.Label(self, text=joint_name.replace("_", " ").capitalize(), font=('Helvetica', 10, 'bold'))
        self.joint_idx = joint_idx
        self.increase_angle_btn = ttkb.Button(self, text=">", command=self.increase_joint_angle)
        self.decrease_angle_btn = ttkb.Button(self, text="<", command=self.decrease_joint_angle)
        self.increase_speed_btn = ttkb.Button(self, text="+", command=self.increase_speed)
        self.decrease_speed_btn = ttkb.Button(self, text="-", command=self.decrease_speed)
        value = ttkb.Label(self, textvariable=self.joint_value, font=('Helvetica', 12, 'bold'))
        label.pack()
        value.pack()
        self.increase_angle_btn.pack(side='right')
        self.decrease_angle_btn.pack(side='left')
        self.increase_speed_btn.pack(side='right')
        self.decrease_speed_btn.pack(side='right')
        self.cb = cb
        self.getIncrement = getIncrement

    def set_joint_value(self):
        self.cb(self.joint_idx)

    def increase_joint_angle(self):
        current_value = self.joint_value.get()
        new_value = current_value + self.getIncrement()
        if new_value > self.joint_range[1]:
            return
        else:
            self.joint_value.set(current_value + self.getIncrement())
            self.set_joint_value()

    def decrease_joint_angle(self):
        current_value = self.joint_value.get()
        new_value = current_value - self.getIncrement()
        if new_value < self.joint_range[0]:
            return
        else:
            self.joint_value.set(current_value - self.getIncrement())
            self.set_joint_value()

    def increase_speed(self):
        pass
    def decrease_speed(self):
        pass

