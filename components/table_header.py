import ttkbootstrap as ttk

class TableHeader(ttk.Frame):
    def __init__(self, parent, name, labels):
        super().__init__(parent, name=name)
        self.parent = parent
        self.headers = []

        for i,l in enumerate(labels):
            ttk.Label(self, text=l, width=20).grid(row=0, column=i)

if __name__ == "__main__":
    header = TableHeader(None)
    print(header.headers)