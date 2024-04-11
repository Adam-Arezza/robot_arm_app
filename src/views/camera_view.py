import ttkbootstrap as ttkb


class CameraView(ttkb.Frame):
    def __init__(self, parent):
        super().__init__(parent, borderwidth=2, relief=ttkb.constants.GROOVE)
        self.header = ttkb.Label(self, text='Camera Viewer', font=('bold', 12))
        self.header.pack(anchor='nw')
        self.name = 'camera_view'
