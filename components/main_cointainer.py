import ttkbootstrap as ttk

class MainContainer:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(self.parent, width=800, height=500, name='main_frame')
        self.frame.pack(side='left', anchor='nw', expand=True, fill='both')
        self.frame.pack_propagate(0)