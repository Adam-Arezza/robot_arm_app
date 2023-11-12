import ttkbootstrap as ttk


class RobotConfig(ttk.Frame):
    def __init__(self, parent, robot_config):
        super().__init__(parent)
        self.robot_config = robot_config
        self.font = ttk.font.Font(size=12)
        self.rows = []
        for i,j in enumerate(robot_config):
            row = ttk.Frame(self)
            row.pack(fill='x')
            t,a,r,d = robot_config[f'{j}']
            theta_label = ttk.Label(row, text=f'{t}', width=20, font=self.font)
            alpha_label = ttk.Label(row, text=f'{a}', width=20, font=self.font)
            r_label = ttk.Label(row, text=f'{r}', width=20, font=self.font)
            d_label = ttk.Label(row, text=f'{d}', width=20, font=self.font)
            theta_label.pack(side='left')
            alpha_label.pack(side='left')
            r_label.pack(side='left')
            d_label.pack(side='left')
