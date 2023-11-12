import ttkbootstrap as ttk
from components.joint_slider import JointSlider
from components.serial_connector import SerialConnector

class SideMenu(ttk.Frame):
    def __init__(self, parent, sim_cb, save_rb, teach_cb, show_cb):
        super().__init__(parent, padding=10, style='secondary.TFrame', name='menu_frame')
        self.parent = parent

        # callback functions
        self.sim_cb = sim_cb
        self.save_robot = save_rb     
        self.teach_cb = teach_cb
        self.show_cb = show_cb

        #self.font_style = ttk.font.Font(size=12)
        #self.font = ttk.Style.theme_create(themename='btn_font')
        #self.font.configure('btn_font', font=self.font_style)
        #menu buttons
        self.simulate_robot_btn = ttk.Button(self, text='Simulate', width=30, command=self.sim_robot)
        
        self.save_robot_btn = ttk.Button(self, text='Save Robot', width=30, command=self.save_robot)
        
        self.save_routine_btn = ttk.Button(self, text='Save Routine', width=30,command=self.save_routine)

        self.teach_pendant_btn = ttk.Button(self, text='Teach Pendant', width=30, command=self.teach_cb)

        self.show_robot_btn = ttk.Button(self, text='Show Robot', width=30, command=self.show_cb)
       
        self.serial_connector = SerialConnector(self)
        
        # button layout
        self.show_robot_btn.pack(side='top', pady=8)
        self.simulate_robot_btn.pack(side='top')
        self.save_robot_btn.pack(side='top', pady=8)
        self.save_routine_btn.pack(side='top')
        self.teach_pendant_btn.pack(side='top', pady=8)

        self.serial_connector.pack()

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