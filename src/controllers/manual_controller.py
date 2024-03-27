from src.views.manual_controls_view import ManualControls

class ManualController:
    def __init__(self, root, parent):
        self.view = ManualControls(parent,4)

    def show_view(self):
       # self.view.pack(anchor='ne', side='right', expand=True, fill='both')
       self.view.grid(column=2, row=1, sticky='nsew')
