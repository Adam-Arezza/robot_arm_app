import ttkbootstrap as ttk

class SideMenu:
    def __init__(self, parent, sim_cb):
        self.parent = parent
        self.sim_cb = sim_cb
        self.frame = ttk.Frame(parent, 
                               style='secondary.TFrame', 
                               padding=10, 
                               width=200, 
                               height=1000,
                               name='menu_frame')
        self.frame.pack(side='left', fill='both', expand=True)
        
        self.simulate_robot_btn = ttk.Button(self.frame, 
                                           text='Simulate',
                                           command=self.sim_robot)

        self.load_robot_btn = ttk.Button(self.frame,
                                         text='Load Robot',
                                         command=self.load_robot)
        
        self.save_robot_btn = ttk.Button(self.frame,
                                         text='Save Robot',
                                         command=self.save_robot)
        
        self.save_routine_btn = ttk.Button(self.frame,
                                           text='Save Routine',
                                           command=self.save_routine)
        
        self.simulate_robot_btn.pack(side='top', pady=8, fill='x')
        self.load_robot_btn.pack(side='top', fill='x')
        self.save_robot_btn.pack(side='top', pady=8, fill='x')
        self.save_routine_btn.pack(side='top', fill='x')


    def load_robot(self):
        print('loading robot!')

    def save_robot(self):
        print('Saving robot!')

    def save_routine(self):
        print('Saving Routine!')
    
    def sim_robot(self):
        self.sim_cb()