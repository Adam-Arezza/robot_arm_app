from src.views.goal_point_view import GoalPointView
from ttkbootstrap.dialogs import Messagebox


class PointsHandler:
    def __init__(self, root, parent):
        self.points = {}
        self.id_counter = 0
        self.view = GoalPointView(parent, self.preview_point)
        self.root = root
        self.view.points_button_group.buttons["define_point"].configure(command=self.create_point)
        self.view.points_button_group.buttons["cancel"].configure(command=self.cancel_goal_point)
        self.view.points_button_group.buttons["go_to_goal"].configure(command=self.go_to_goal)


    def preview_point(self):
        point = self.get_point()
        self.root.main_container.robot_handler.preview_point(point)


    def create_point(self):
        point = self.get_point()
        valid_point = self.root.main_container.robot_handler.check_valid_point(point)
        if valid_point:
            self.root.main_container.robot_handler.add_goal_point(point)
            new_id = self.id_counter
            self.points[new_id] = point
            self.view.points_table.insert_row(values=[new_id,point])
            self.view.points_table.load_table_data()
            self.id_counter += 1
        else:
            Messagebox.ok('Invalid point, robot cannot reach the desired goal.')
            return


    def get_point(self):
        return [round(float(self.view.x.get()),3), round(float(self.view.y.get()),3), round(float(self.view.z.get()),3)]


    def cancel_goal_point(self):
        self.root.main_container.robot_handler.clear_point_preview()


    def go_to_goal(self):
        #get goal from table selection
        table_rows = self.view.points_table.get_rows(selected=True)
        goal = []
        for row in table_rows:
            goal.append(row.values[1])
        self.root.main_container.robot_handler.go_to_goal(goal)

