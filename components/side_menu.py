import ttkbootstrap as ttk

class SideMenu:
    def __init__(self, parent, sim_cb, save_rb, load_rb):
        self.parent = parent
        self.sim_cb = sim_cb
        self.save_robot = save_rb
        self.load_robot = load_rb
        self.frame = ttk.Frame(parent,  
                               padding=10,
                               style='secondary.TFrame',
                               width=200,
                               name='menu_frame')
        self.frame.pack(side='left', fill='both', expand=False)
        self.frame.pack_propagate(0)
        
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

    def save_routine(self):
        print('Saving Routine!')
    
    def sim_robot(self):
        self.sim_cb()
    