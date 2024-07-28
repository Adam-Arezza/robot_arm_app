import ttkbootstrap as ttkb
from src.serial_service import SerialService
from src.handlers.menu_handler import MenuHandler
from src.handlers.robot_handler import RobotHandler
from src.handlers.start_view_handler import StartViewHandler
from src.handlers.serial_handler import SerialHandler
from src.handlers.joint_table_handler import JointTableHandler
from src.handlers.controls_handler import ControlsHandler
from src.utils import to_degrees, to_radians
from ttkbootstrap.dialogs.dialogs import Messagebox
from src.views.camera_view import CameraView
from src.robot_model import RobotArm


class MainContainer(ttkb.Frame):
    def __init__(self, root):
        super().__init__(root, style='secondary.TFrame')
        self.root = root
        self.serial_service = SerialService()
        self.main_grid_frame = ttkb.Frame(self)
        self.start_handler = StartViewHandler(root,self)
        self.menu_handler = MenuHandler(root)
        self.start_handler.show_view()
        self.notebook = ttkb.Notebook(self.main_grid_frame)

        #configure the main grid layout
        self.main_grid_frame.columnconfigure(1, weight=1)
        self.main_grid_frame.columnconfigure(0, weight=1)
        self.main_grid_frame.rowconfigure(0, weight=1)         
        self.main_grid_frame.rowconfigure(1, weight=1)


    def main_view(self, model:RobotArm):
        self.root.config(menu=self.menu_handler.view)
        self.robot_model = model
        self.add_handlers()
        self.start_handler.kill_view()
        self.camera_view = CameraView(self.notebook)
        self.main_grid_frame.grid(column=0, row=0, rowspan=2, columnspan=2, sticky="nsew")
        self.notebook.add(self.joint_table_handler.view, text="Joint configurations")
        self.notebook.add(self.serial_handler.view, text="Serial")
        self.notebook.add(self.camera_view, text="Vision")
        self.notebook.grid(column=0,row=0, rowspan=2, sticky='nsew')
        self.robot_handler.view.grid(column=1, row=0, columnspan=2,rowspan=1, sticky='nsew')
        self.controls_handler.view.grid(column=1, row=1, sticky='n')
        self.create_serial_subscriptions()
        self.joint_table_handler.create_joint_entries(len(self.robot_model.links))
        self.robot_handler.set_joints(self.robot_model.robot.q)


    def create_serial_subscriptions(self):
        self.serial_service.add_subscriber('new_data', self.robot_handler.update_joint_data)
        self.serial_service.add_subscriber('connected', self.serial_handler.add_serial_connection)
        self.serial_service.add_subscriber('disconnected', self.serial_handler.remove_serial_connection)
        self.serial_service.add_subscriber('new_target', self.robot_handler.set_new_target)
        self.serial_service.add_subscriber('log', self.serial_handler.log_message)


    def add_handlers(self):
        #handlers
        self.robot_handler = RobotHandler(self.root, 
                                                self.main_grid_frame, 
                                                self.serial_service,
                                                self.robot_model)
        self.joint_table_handler = JointTableHandler(self.root, 
                                                           self.serial_service, 
                                                           self.notebook)
        self.serial_handler = SerialHandler(self.root,
                                            self.serial_service, 
                                            self.notebook)
        self.controls_handler = ControlsHandler(self.root, 
                                                      self.main_grid_frame, 
                                                      self.serial_service,
                                                      self.robot_model)


    def on_close(self):
        self.robot_handler.view.close()
        self.serial_service.disconnect()
        print("Shutting down...")
        self.destroy()

