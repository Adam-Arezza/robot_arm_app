import ttkbootstrap as ttk

class ButtonGroup(ttk.Frame):
    def __init__(self, parent, buttons):
        super().__init__(parent, name='dh_table_btn_group')

        self.buttons = {}
        for button in buttons:
            b = ttk.Button(self, text=button[0], command=button[1])
            self.buttons[f'{button[0]}'] = b
            b.pack(side='left', padx=10)
        
        print(self.buttons)
        # self.add_link_btn = ttk.Button(self.btn_frame, text='Add Link', command=self.add_link)
        # self.add_link_btn.pack(side='left', padx=10)

        # self.clear_table_btn = ttk.Button(self.btn_frame, text='Clear', command=self.clear_table)
        # self.clear_table_btn.pack(side='left')

        # self.create_robot_btn = ttk.Button(self.btn_frame, text='Create Robot', command=self.create_robot)
        # self.create_robot_btn.pack(side='left', padx=10)