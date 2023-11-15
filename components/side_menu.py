import ttkbootstrap as ttk
from components.joint_slider import JointSlider
from components.serial_connector import SerialConnector

class SideMenu(ttk.Frame):
    def __init__(self, parent, save_rb, teach_cb, show_cb):
        super().__init__(parent, padding=10, style='secondary.TFrame', name='menu_frame')
        self.parent = parent

        # callback functions
        self.save_robot = save_rb     
        self.teach_cb = teach_cb
        self.show_cb = show_cb
        
        #menu buttons  
        self.save_robot_btn = ttk.Button(self, text='Save Robot', width=30, command=self.save_robot) 
        
        self.teach_pendant_btn = ttk.Button(self, text='Teach Pendant', width=30, command=self.teach_cb)

        self.show_robot_btn = ttk.Button(self, text='Show Robot', width=30, command=self.show_cb)
       
        self.serial_connector = SerialConnector(self)
        
        # button layout
        self.show_robot_btn.pack(side='top', pady=8)
        self.save_robot_btn.pack(side='top', pady=8) 
        self.teach_pendant_btn.pack(side='top', pady=8)

        self.serial_connector.pack()