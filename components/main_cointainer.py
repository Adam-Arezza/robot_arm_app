import ttkbootstrap as ttk

class MainContainer:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(self.parent, width=1000, height=500, name='main_frame')
        self.frame.pack(fill='x',expand=1)