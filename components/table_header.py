import ttkbootstrap as ttk

class TableHeader:
    def __init__(self, parent, layout):
        self.parent = parent
        self.headers = []
        self.layout = layout
        self.frame = ttk.Frame(self.parent, name='table_header_frame')
        self.frame.pack(anchor='nw', pady=10)

        theta = ttk.Label(self.frame, text='Theta (deg)', width=20)
        alpha = ttk.Label(self.frame, text='Alpha (deg)', width=20)
        r = ttk.Label(self.frame, text='r (m)', width=20)
        d = ttk.Label(self.frame, text='d (m)', width=20)

        self.headers.append(theta)
        self.headers.append(alpha)
        self.headers.append(r)
        self.headers.append(d)

        if self.layout == 'p':
            self.pack_layout()
        
        if self.layout == 'g':
            self.grid_layout()
        
    def grid_layout(self):
        for i, h in enumerate(self.headers):
            h.grid(row=0, column=i, padx=5)
    
    def pack_layout(self):
        for i, h in enumerate(self.headers):
            h.pack(side='left', padx=20, anchor='nw')

if __name__ == "__main__":
    header = TableHeader(None)
    print(header.headers)