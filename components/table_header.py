import ttkbootstrap as ttk

class TableHeader:
    def __init__(self, parent):
        self.parent = parent
        self.headers = []
        self.frame = ttk.Frame(self.parent, name='table_header_frame')
        # self.frame.grid(row=0, column=0)
        self.frame.pack(anchor='nw', padx= 70)

        theta = ttk.Label(self.frame, text='Theta')
        alpha = ttk.Label(self.frame, text='Alpha')
        r = ttk.Label(self.frame, text='r')
        d = ttk.Label(self.frame, text='d')

        self.headers.append(theta)
        self.headers.append(alpha)
        self.headers.append(r)
        self.headers.append(d)

        # for i, h in enumerate(self.headers):
        #     h.grid(row=0, column=i)
        
        for i, h in enumerate(self.headers):
            h.pack(side='left', padx=50, anchor='nw')

if __name__ == "__main__":
    header = TableHeader(None)
    print(header.headers)