import ttkbootstrap as ttkb
from src.views.components.button_group import ButtonGroup
#from src.views.d_h_table import DHTable
from PIL import Image, ImageTk
import json

class StartView(ttkb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.image = Image.open('assets/robot.png')
        width = self.image.width
        height = self.image.height
        self.robot_img = self.image.resize((int(width/3), int(height/3)))
        self.robot_image = ImageTk.PhotoImage(self.robot_img)
        self.image_label = ttkb.Label(self,image=self.robot_image)
        self.image_label.pack(pady=(100,0))
        self.controller = controller
        self.initial_btns = ButtonGroup(self,
                                        buttons=[('Create DH robot', self.controller.create_dh_robot),
                                                 ('Load robot', self.controller.load_robot)],
                                        container_style='default')
        self.initial_btns.pack(pady=30)