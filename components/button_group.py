import ttkbootstrap as ttk

class ButtonGroup(ttk.Frame):
    def __init__(self, parent, buttons, container_style, style=None, horizontal=False):
        super().__init__(parent, name='dh_table_btn_group', height=300, width=400, style=container_style)

        self.buttons = {}
        self.style = None
        if style:
            self.style = style
        else:
            self.style = 'default'
        for button in buttons:
            b = ttk.Button(self, text=button[0], command=button[1], bootstyle=self.style)
            self.buttons[f'{button[0]}'] = b
            if horizontal:
                b.pack(side='left', padx=10)
            else:
                b.pack(pady=10, fill='x')
