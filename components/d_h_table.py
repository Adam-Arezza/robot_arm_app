import ttkbootstrap as ttk
from components.table_row import TableRow
from components.table_header import TableHeader

class DHTable():
    def __init__(self, parent, cb):
        self.parent = parent
        self.cb = cb
        self.btn_frame = ttk.Frame(self.parent, name='table_btns')
        self.btn_frame.pack(anchor='nw')

        self.table_title = ttk.Label(self.btn_frame, text='D-H Parameters', font='bold')
        self.table_title.pack(padx=(50, 5), pady=10)

        self.add_row_btn = ttk.Button(self.btn_frame, text='Add Row', command=self.add_row)
        self.add_row_btn.pack(side='left', padx=10)

        self.clear_table_btn = ttk.Button(self.btn_frame, text='Clear', command=self.clear_table)
        self.clear_table_btn.pack(side='left')

        self.create_robot_btn = ttk.Button(self.btn_frame, 
                                           text='Create Robot',
                                           command=self.create_robot)
        self.create_robot_btn.pack(side='left', padx=10)
        
        # self.print_btn = ttk.Button(self.parent, text='print', command=self.print_table)
        # self.print_btn.pack()

        self.table_header = TableHeader(self.parent)

        self.table_frame = ttk.Frame(self.parent, name='table_frame')
        self.table_frame.pack(anchor='nw')
        
        self.rows = []
        new_row = TableRow(self.table_frame, 'Joint_1')
        self.rows.append(new_row)

        for i in range(len(self.rows)):
            self.rows[i].grid(row=i+1, column=0)

    def add_row(self):
        current_row = len(self.rows)
        if current_row >= 6:
            self.add_row_btn.setvar("state", "disabled")
            return 
        new_row = TableRow(self.table_frame, f'Joint_{current_row + 1}')
        self.rows.append(new_row)
        self.rows[-1].grid(row=current_row+1, column=0)
    
    def print_table(self):
        rows = self.rows
        print('D-H Parameters')
        print(f'Joint | Theta | Alpha | r | d |')
        for row in rows:
            print(row)
            print_row = []
            print_row.append(row.joint)
            for p in row.params:
                print_row.append(p.get())
            print(print_row)
    
    def clear_table(self):
        for row in self.rows:
            row.destroy()
        
        self.rows = []
        new_row = TableRow(self.table_frame, 'Joint_1')
        self.rows.append(new_row)

        for i in range(len(self.rows)):
            self.rows[i].grid(row=i, column=0)
    
    def create_robot(self):
        rows = self.rows
        params = {}
        for row in rows:
            print_row = []
            print_row.append(row.joint)
            for p in row.params:
                print_row.append(p.get())
            print(print_row)
            params[f'{row.joint}'] = print_row
        self.cb(params)
