import ttkbootstrap as ttk

class ButtonGroup(ttk.Frame):
    def __init__(self, parent, buttons):
        super().__init__(parent, name='dh_table_btn_group', height=300, width=400)

        self.buttons = {}
        for button in buttons:
            b = ttk.Button(self, text=button[0], command=button[1])
            self.buttons[f'{button[0]}'] = b
            b.pack(side='left', padx=10)
