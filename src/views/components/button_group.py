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
            btn_name = button[0].replace(" ", "_").lower()
            b = ttkb.Button(self, 
                            text=button[0], 
                            style='primary.Outline.TButton', 
                            padding=(8,3), 
                            name=btn_name)
            if len(button) == 2:
                b.configure(command=button[1])
            self.buttons[f'{btn_name}'] = b
            if horizontal:
                b.pack(side='left', padx=0, pady=0)
            else:
                b.pack(fill='x', pady=10, padx=20)
