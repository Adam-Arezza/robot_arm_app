import ttkbootstrap as ttk

class SideMenu:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent, style='secondary.TFrame', padding=10)
        self.frame.pack(side='left', fill='y')

        self.create_robot_btn = ttk.Button(self.frame, 
                                           text='Create Robot',
                                           command=self.create_robot)
        

        self.load_robot_btn = ttk.Button(self.frame,
                                         text='Load Robot',
                                         command=self.load_robot)
        
        self.save_robot_btn = ttk.Button(self.frame,
                                         text='Save Robot',
                                         command=self.save_robot)
        
        self.save_routine_btn = ttk.Button(self.frame,
                                           text='Save Routine',
                                           command=self.save_routine)
        
        self.create_robot_btn.pack(side='top')
        self.load_robot_btn.pack(side='top', pady=8, fill='x')
        self.save_robot_btn.pack(side='top', fill='x')
        self.save_routine_btn.pack(side='top', pady=8, fill='x')
    
    def create_robot(self):
        print('Time to create a new robot!')
    
    def load_robot(self):
        print('loading robot!')

    def save_robot(self):
        print('Saving robot!')

    def save_routine(self):
        print('Saving Routine!')