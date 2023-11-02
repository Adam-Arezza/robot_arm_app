import ttkbootstrap as ttk
from components.table_row import TableRow
from components.table_header import TableHeader

class DHTable:
    def __init__(self, parent, cb):
        self.parent = parent
        self.cb = cb
        self.btn_frame = ttk.Frame(self.parent, name='table_btns')
        self.btn_frame.pack(anchor='nw')

        self.table_title = ttk.Label(self.btn_frame, text='D-H Parameters', font='bold')
        self.table_title.pack(padx=(50, 5), pady=10)

        self.add_link_btn = ttk.Button(self.btn_frame, text='Add Link', command=self.add_link)
        self.add_link_btn.pack(side='left', padx=10)

        self.clear_table_btn = ttk.Button(self.btn_frame, text='Clear', command=self.clear_table)
        self.clear_table_btn.pack(side='left')

        self.create_robot_btn = ttk.Button(self.btn_frame, 
                                           text='Create Robot',
                                           command=self.create_robot)
        self.create_robot_btn.pack(side='left', padx=10)

        self.table_header = TableHeader(self.parent, 'p')

        self.table_frame = ttk.Frame(self.parent, name='table_frame')
        self.table_frame.pack(anchor='nw')
        
        self.rows = []
        new_row = TableRow(self.table_frame, 'Joint_1')
        self.rows.append(new_row)

        for i in range(len(self.rows)):
            self.rows[i].grid(row=i+1, column=0)

    def add_link(self):
        current_row = len(self.rows)
        if current_row >= 6:
            self.add_link_btn.setvar("state", "disabled")
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
            dh_parameters = []
            dh_parameters.append(row.joint)
            for p in row.params:
                dh_parameters.append(p.get())
            print(dh_parameters)
    
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
            dh_parameters = []
            dh_parameters.append(row.joint)
            for p in row.params:
                dh_parameters.append(p.get())
            # print(dh_parameters)
            dh_parameters.pop(0)
            params[f'{row.joint}'] = dh_parameters
        self.cb(params)
    
    def destroy_all(self):
        self.table_frame.destroy()
        self.btn_frame.destroy()
        self.rows = []
        self.table_header.frame.destroy()
