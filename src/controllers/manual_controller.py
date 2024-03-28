
class ManualController:
    def __init__(self, root):
        self.view = None


    def add_view(self, view):
        self.view = view


    def pack_view(self):
        self.view.pack(side='left')


    def get_slider_values(self):
        sliders = self.view.gets_slider_values()
        print(sliders)

    def kill_view(self):
        self.view.destroy()
