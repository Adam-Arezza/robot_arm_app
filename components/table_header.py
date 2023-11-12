import ttkbootstrap as ttk

class TableHeader(ttk.Frame):
    def __init__(self, parent, name, labels):
        super().__init__(parent, name=name)
        self.parent = parent
        self.headers = []
        self.font = ttk.font.Font(size=12)
        for i,l in enumerate(labels):
            ttk.Label(self, text=l, width=20, font=self.font).grid(row=0, column=i)
