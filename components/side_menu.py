import ttkbootstrap as ttk
from components.joint_slider import JointSlider

class SideMenu(ttk.Frame):
    def __init__(self, parent, sim_cb, save_rb, teach_cb):
        super().__init__(parent, padding=10, style='secondary.TFrame', width=200, name='menu_frame')
        self.parent = parent

        # callback functions
        self.sim_cb = sim_cb
        self.save_robot = save_rb     
        self.teach_cb = teach_cb

        #menu buttons
        self.simulate_robot_btn = ttk.Button(self, text='Simulate', command=self.sim_robot)
           
        self.save_robot_btn = ttk.Button(self, text='Save Robot', command=self.save_robot)
        
        self.save_routine_btn = ttk.Button(self, text='Save Routine', command=self.save_routine)

        self.teach_pendant_btn = ttk.Button(self,
                                            text='Teach Pendant',
                                            command=self.teach_cb)
        
        # button layout
        self.simulate_robot_btn.pack(side='top', pady=8, fill='x')
        self.save_robot_btn.pack(side='top', fill='x')
        self.save_routine_btn.pack(side='top',pady=8, fill='x')
        self.teach_pendant_btn.pack(side='top', fill='x')

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