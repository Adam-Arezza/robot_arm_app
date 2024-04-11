from src.utils import find

class LayoutManager:
    def __init__(self):
        self.views = []
        self.main_grid = None

    def add_view(self, view):
        self.views.append(view)


    def add_main_grid(self, view):
        self.main_grid = view
        self.main_grid.columnconfigure(0, weight=1)
        self.main_grid.columnconfigure(1, weight=1)
        self.main_grid.rowconfigure(0, weight=1)
        self.main_grid.rowconfigure(1, weight=1)


    def create_main_grid(self):
        self.main_grid.grid(column=0, row=0, rowspan=2, columnspan=2, sticky="nsew")

    
    def create_grid(self):
        serial_view = find(self.views, lambda v: v.name == 'serial_view')
        joint_table_view = find(self.views, lambda v: v.name == 'joint_table_view')
        robot_view = find(self.views, lambda v: v.name == 'robot_view')
        
        serial_view.grid(column=0, row=0,rowspan=2, sticky='nsew')
        robot_view.grid(column=1, row=0, sticky='nsew')
        joint_table_view.grid(column=1, row=1, sticky='nsew')

       # num_columns = cols
       # num_rows = rows
       # grid_counter = 0
       # for i in range(num_columns):
       #     for n in range(num_rows):
       #         self.views[grid_counter].grid(column=i, row=n, sticky="nsew")
       #         grid_counter += 1


