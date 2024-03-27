from src.views.manual_controls_view import ManualControls

class ManualController:
    def __init__(self, root):
        #self.view = ManualControls(parent,4)
        print("initialized manual controller")


    def add_view(self, view):
        self.view = view


    def show_view(self):
       # self.view.pack(anchor='ne', side='right', expand=True, fill='both')
       self.view.grid(column=2, row=1, sticky='nsew')
