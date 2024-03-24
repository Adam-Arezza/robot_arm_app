from src.utils import to_radians


class RobotController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

    def show_robot(self):
        self.model.robot.plot(self.model.robot.q)

    def teach_pendant(self):
        self.model.robot.teach(self.model.robot.q)

    def show_joint_config(self,cfg):
        old_config = self.model.robot.q
        self.model.robot.q = to_radians(cfg)
        self.model.robot.plot(self.model.robot.q)
        self.model.robot.q = old_config

    def show_trajectory(self,traj):
        self.model.robot.plot(traj)


    def reset(self):
        self.model.robot.q = self.model.default_state


    def set_joints(self, joints):
        self.model.robot.q = joints

    def get_joints(self):
        return self.model.robot.q

    def show_view(self):
        self.view.pack(side='right', fill='x', padx=0, pady=0)

    def kill_view(self):
        self.view.close()
        self.view.destroy()
