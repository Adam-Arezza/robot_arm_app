from src.views.manual_controls_view import ManualControls

class ManualController:
    def __init__(self, root):
        self.view = None


    def add_view(self, view):
        self.view = view


    def kill_view(self):
        self.view.destroy()
