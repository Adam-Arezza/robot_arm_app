import ttkbootstrap as ttk
from components.button_group import ButtonGroup
from components.table_row import TableRow
from components.table_header import TableHeader
from ttkbootstrap.constants import *

class DHTable(ttk.Frame):
    def __init__(self, parent, cb):
        super().__init__(parent)
        self.parent = parent
        self.create_robot_cb = cb

        self.table_title = ttk.Label(self, text='D-H Parameters', font='bold')
        self.table_title.pack(padx=(50, 5), pady=10)

        self.buttons = ButtonGroup(self, [('Add Link', self.add_link), 
                                          ('Create Robot', self.create_robot_cb), 
                                          ('Clear Table', self.clear_table)])
        
        self.buttons.pack(anchor='nw')

        self.header_labels = ['Theta (deg)', 'Alpha (deg)', 'r (m)', 'd (m)']
        self.table_header = TableHeader(self, name='table_headers', labels=self.header_labels)
        
        self.rows = []
        new_row = TableRow(self, 'Joint_1')
        self.rows.append(new_row)

        for i in range(len(self.rows)):
            self.rows[i].pack()

    def add_link(self):
        current_row = len(self.rows)
        if current_row >= 6:
            self.buttons.buttons["Add Link"]['state'] = DISABLED
            return 
        new_row = TableRow(self, f'Joint_{current_row + 1}')
        self.rows.append(new_row)
        new_row.pack()
    
    def clear_table(self):
        for row in self.rows:
            row.destroy()
        
        self.rows = []
        new_row = TableRow(self, 'Joint_1')
        self.rows.append(new_row)
        new_row.pack()
        self.buttons.buttons["Add Link"]['state'] = NORMAL

        # for i in range(len(self.rows)):
        #     self.rows[i].grid(row=i, column=0)
    
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
