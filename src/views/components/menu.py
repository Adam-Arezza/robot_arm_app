import ttkbootstrap as ttkb


class Menu(ttkb.Menu):
    def __init__(self, root, config, handler):
        super().__init__(root)
        self.handler = handler
        self.config = config
        self.file_menu = ttkb.Menu(root)
        self.file_menu.add_command(label='Create', command=self.handler.create_robot)
        self.file_menu.add_command(label='Save', command=self.handler.save_robot)
        self.file_menu.add_command(label='Load', command=self.handler.load_robot)
        self.file_menu.add_command(label='Exit', command=self.handler.exit)
        self.add_cascade(label="File", menu=self.file_menu)
        self.add_command(label="Tool Tip", command=self.handler.open_calibration)
        self.add_command(label="Generate Pose Data", command=self.handler.open_pose_generator)
        self.add_command(label="Help", command=self.handler.show_help_dialog)

        
