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
from src.layout_manager import LayoutManager
from src.robot_model import RobotArm


class MainContainer(ttkb.Frame):
    def __init__(self, root):
        super().__init__(root, style='secondary.TFrame')
        self.root = root
        self.serial_service = SerialService()
        self.layout_mgr = LayoutManager()
        self.main_grid_frame = ttkb.Frame(self)
        self.start_handler = StartViewHandler(root,self)
        self.menu_handler = MenuHandler(root)
        self.start_handler.show_view()


    def main_view(self, model:RobotArm):
        self.root.config(menu=self.menu_handler.view)
        self.robot_model = model
        self.add_handlers()
        self.start_handler.kill_view()
        self.initialize_layout_manager()
        num_joints = len(self.robot_model.robot.links)
        self.create_serial_subscriptions()
        self.joint_table_handler.create_joint_entries(num_joints)
        self.robot_handler.set_joints(self.robot_model.robot.q)


    def create_serial_subscriptions(self):
        self.serial_service.add_subscriber('new_data', self.serial_handler.update_serial_window_received)
        self.serial_service.add_subscriber('new_data', self.robot_handler.update_joint_data)
        self.serial_service.add_subscriber('connected', self.serial_handler.add_serial_connection)
        self.serial_service.add_subscriber('disconnected', self.serial_handler.remove_serial_connection)
        self.serial_service.add_subscriber('send', self.serial_handler.update_serial_window_sent)
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
                                                           self.main_grid_frame)
        self.serial_handler = SerialHandler(self.root,
                                            self.serial_service, 
                                            self.main_grid_frame)
        self.controls_handler = ControlsHandler(self.root, 
                                                      self.main_grid_frame, 
                                                      self.serial_service,
                                                      self.robot_model)

    def initialize_layout_manager(self):
        #add views to layout manager
        self.layout_mgr.add_main_grid(self.main_grid_frame)
        self.layout_mgr.add_view(self.serial_handler.view)
        self.layout_mgr.add_view(self.joint_table_handler.view)
        self.layout_mgr.add_view(self.robot_handler.view)
        #self.layout_mgr.add_view(self.camera_view)
        self.layout_mgr.add_view(self.controls_handler.view)
        self.layout_mgr.create_main_grid()
        self.layout_mgr.create_grid()


    def on_close(self):
        for view in self.layout_mgr.views:
            view.destroy()
        self.robot_handler.view.close()
        self.layout_mgr.main_grid.destroy()
        self.serial_service.disconnect()
        print("Shutting down...")
        self.destroy()

