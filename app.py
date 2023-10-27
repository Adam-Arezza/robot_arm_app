import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class App:
    def __init__(self, root):
        self.root = root
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App(ttk.Window(themename="darkly"))
    app.run()