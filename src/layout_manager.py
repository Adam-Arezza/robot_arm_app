class LayoutManager:
    def __init__(self):
        self.views = []


    def add_view(self, view):
        self.views.append(view)

    def create_grid(self, cols, rows):

        if rows * cols != len(self.views):
            print("views won't fit in grid")
            return
        num_columns = cols
        num_rows = rows
        grid_counter = 0

        for i in range(num_columns):
            for n in range(num_rows):
                self.views[grid_counter].grid(column=i, row=n, sticky="nsew")
                grid_counter += 1


