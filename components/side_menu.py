import ttkbootstrap as ttk
from components.joint_slider import JointSlider

class SideMenu(ttk.Frame):
    def __init__(self, parent, sim_cb, save_rb, load_rb):
        super().__init__(parent, padding=10, style='secondary.TFrame', width=200, name='menu_frame')
        self.parent = parent

        # callback functions
        self.sim_cb = sim_cb
        self.save_robot = save_rb
        self.load_robot = load_rb

        #menu buttons
        self.simulate_robot_btn = ttk.Button(self, text='Simulate', command=self.sim_robot)

        self.load_robot_btn = ttk.Button(self, text='Load Robot', command=self.load_robot)
        
        self.save_robot_btn = ttk.Button(self, text='Save Robot', command=self.save_robot)
        
        self.save_routine_btn = ttk.Button(self, text='Save Routine', command=self.save_routine)
        
        # button layout
        self.simulate_robot_btn.pack(side='top', pady=8, fill='x')
        self.load_robot_btn.pack(side='top', fill='x')
        self.save_robot_btn.pack(side='top', pady=8, fill='x')
        self.save_routine_btn.pack(side='top', fill='x')

        self.sliders = []

    def save_routine(self):
        print('Saving Routine!')
    
    def sim_robot(self):
        self.sim_cb()
    
    def add_sliders(self):
        for i in range(4):
            slider = JointSlider(self, joint_name=f'joint_{i}')
            slider.pack(anchor='nw', pady=15, fill='x')
            self.sliders.append(slider)
    