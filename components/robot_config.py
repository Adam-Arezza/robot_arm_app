import ttkbootstrap as ttk


class RobotConfig(ttk.Frame):
    def __init__(self, parent, robot_config):
        super().__init__(parent, borderwidth=10, relief=ttk.GROOVE)
        self.robot_config = robot_config
        self.pack(anchor='nw')
        self.rows = []
        for i,j in enumerate(robot_config):
            row = ttk.Frame(self)
            row.pack(fill='x')
            t,a,r,d = robot_config[f'{j}']
            theta_label = ttk.Label(row, text=f'{t}', width=20)
            alpha_label = ttk.Label(row, text=f'{a}', width=20)
            r_label = ttk.Label(row, text=f'{r}', width=20)
            d_label = ttk.Label(row, text=f'{d}', width=20)
            theta_label.pack(side='left')
            alpha_label.pack(side='left')
            r_label.pack(side='left')
            d_label.pack(side='left')
