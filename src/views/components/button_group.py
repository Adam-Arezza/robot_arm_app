import ttkbootstrap as ttkb

class ButtonGroup(ttkb.Frame):
    def __init__(self, parent, buttons, container_style, style=None, horizontal=False):
        super().__init__(parent, style=container_style)

        self.buttons = {}
        self.style = None
        if style:
            self.style = style
        else:
            self.style = 'default'
        for button in buttons:
            b = ttkb.Button(self, text=button[0], command=button[1], style=self.style, padding=(10,10))
            self.buttons[f'{button[0]}'] = b
            if horizontal:
                b.pack(side='left', padx=10, pady=10)
            else:
                b.pack(fill='x', pady=10, padx=10)
