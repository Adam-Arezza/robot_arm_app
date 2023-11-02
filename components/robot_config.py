import ttkbootstrap as ttk


class RobotConfig:
    def __init__(self, parent, robot_config):
        self.parent = parent
        self.robot_config = robot_config
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill='x')
        self.rows = []
        for i,j in enumerate(robot_config):
            row = ttk.Frame(self.frame)
            row.pack(fill='x')
            t,a,r,d = robot_config[f'{j}']
            theta_label = ttk.Label(row, text=f'{t}', width=20)
            alpha_label = ttk.Label(row, text=f'{a}', width=20)
            r_label = ttk.Label(row, text=f'{r}', width=20)
            d_label = ttk.Label(row, text=f'{d}', width=20)
            theta_label.pack(side='left', padx=5)
            alpha_label.pack(side='left', padx=5)
            r_label.pack(side='left', padx=5)
            d_label.pack(side='left', padx=5)
