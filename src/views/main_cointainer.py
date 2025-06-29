import ttkbootstrap as ttkb
from src.serial_service import SerialService
from src.handlers.menu_handler import MenuHandler
from src.handlers.robot_handler import RobotHandler
from src.handlers.start_view_handler import StartViewHandler
from src.handlers.serial_handler import SerialHandler
from src.handlers.joint_table_handler import JointTableHandler
from src.handlers.controls_handler import ControlsHandler
from src.handlers.points_handler import PointsHandler
from ttkbootstrap.dialogs.dialogs import Messagebox
from src.views.camera_view import CameraView
from src.robot_model import RobotArm


class MainContainer(ttkb.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.mode_string = ttkb.StringVar(value='Offline')
        self.mode_value = ttkb.BooleanVar(value=False)
        self.serial_service = SerialService()
        self.main_grid_frame = ttkb.Frame(self)
        self.start_handler = StartViewHandler(root,self)
        self.menu_handler = MenuHandler(root)
        self.start_handler.show_view()
        self.check_btn_frame = ttkb.Frame(self, style='Custom.TFrame')
        self.toggle_label = ttkb.Label(self.check_btn_frame, 
                                       textvariable=self.mode_string, 
                                       style='Custom.TLabel',
                                       font=('Helvetica',10,'bold'))

        self.toggle_mode_switch = ttkb.Checkbutton(self.check_btn_frame,
                                                   onvalue=True,
                                                   offvalue=False,
                                                   variable=self.mode_value,
                                                   style='Custom.TCheckbutton',
                                                   command=self.toggle_online_offline)

        self.reset_btn = ttkb.Button(self.check_btn_frame, 
                                     text="Reset",
                                     style='secondary.TButton',
                                     command=self.reset)
        self.toggle_label.pack(side='left')
        self.toggle_mode_switch.pack(side='left', padx=10, pady=5)
        self.reset_btn.pack(padx=(5,0))

        #configure the main grid layout
        self.main_grid_frame.columnconfigure(0, weight=0)
        self.main_grid_frame.columnconfigure(1, weight=1)
        self.main_grid_frame.columnconfigure(2, weight=1)
        self.main_grid_frame.columnconfigure(3, weight=1)

        self.main_grid_frame.rowconfigure(0, weight=1)
        self.main_grid_frame.rowconfigure(1, weight=1)
        self.main_grid_frame.rowconfigure(2, weight=1)
        self.main_grid_frame.rowconfigure(3, weight=1)



    def main_view(self, model:RobotArm):
        self.root.config(menu=self.menu_handler.view)
        self.robot_model = model
        self.add_handlers()
        self.start_handler.kill_view()
        self.camera_view = CameraView(self.main_grid_frame)
        self.main_grid_frame.grid(column=0, row=0, rowspan=4, columnspan=4, sticky="nsew")
        self.add_notebook_tabs()
        self.check_btn_frame.grid(column=1, row=0, padx=10)
        self.robot_handler.view.grid(column=2, row=0, columnspan=2,rowspan=3, sticky='nsew')
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
                                                           self.main_grid_frame)
        self.serial_handler = SerialHandler(self.root,
                                            self.serial_service, 
                                            self.main_grid_frame)
        self.controls_handler = ControlsHandler(self.root, 
                                                      self.main_grid_frame, 
                                                      self.robot_model)
        self.points_handler = PointsHandler(self.root, self.main_grid_frame)


    def add_notebook_tabs(self):
        self.serial_handler.view.grid(column=0, row=0, columnspan=1)
        self.points_handler.view.grid(column=1, row=0, columnspan=1)
        self.joint_table_handler.view.grid(column=0, row=1, columnspan=1)
        self.controls_handler.view.grid(column=1, row=1)

#toggles robot to online/offline mode
#online will allow robot motion
#offline will show simulated motion
    def toggle_online_offline(self):
        if self.serial_service.serial_connection:
            self.root.set_online_mode(self.mode_value.get())
            self.send_connected_msg()
            self.reset()
        else:
            self.mode_value.set(False)
            Messagebox.ok('Must connect to serial port before going online')


    def reset(self):
        print("resetting")
        self.robot_handler.model.set_joint_states(self.robot_handler.model.default_state)
        sliders = self.controls_handler.view.sliders
        for i in range(len(sliders)):
            sliders[i].slider_value.set(self.robot_handler.model.default_state[i])
            sliders[i].slider.set(self.robot_handler.model.default_state[i])
        if not self.root.online_mode:
            self.root.update_robot_state()
        else:
            command = self.serial_service.format_msg(self.robot_handler.model.default_state)
            self.serial_service.send_serial_msg(command)


    def send_connected_msg(self):
        if self.mode_value.get(): 
            self.mode_string.set('Online')
            go_online_msg = f'<online>'.encode()
            self.serial_service.send_serial_msg(go_online_msg)
        else:
            self.mode_string.set('Offline')

