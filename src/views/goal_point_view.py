import ttkbootstrap as ttkb
from src.views.components.button_group import ButtonGroup


class GoalPointView(ttkb.Frame):
    def __init__(self, parent, preview_point):
        super().__init__(parent, relief=ttkb.constants.GROOVE, borderwidth=2)
        first_row = ttkb.Frame(self)
        x_frame = ttkb.Frame(self)
        y_frame = ttkb.Frame(self)
        z_frame = ttkb.Frame(self)

        self.label = ttkb.Label(first_row,text="XYZ: ", font=('Helvetica', 12, 'bold'))
        self.x = ttkb.StringVar(value=0)
        self.y = ttkb.StringVar(value=0)
        self.z = ttkb.StringVar(value=0)
        self.x_input = ttkb.Entry(first_row, textvariable=self.x)
        self.y_input = ttkb.Entry(first_row, textvariable=self.y)
        self.z_input = ttkb.Entry(first_row, textvariable=self.z)

        self.xlabel = ttkb.Label(x_frame,text="x: ", font=('Helvetica', 10, 'bold'))
        self.ylabel = ttkb.Label(y_frame,text="y: ", font=('Helvetica', 10, 'bold'))
        self.zlabel = ttkb.Label(z_frame,text="z: ", font=('Helvetica', 10, 'bold'))
        self.x_slider = ttkb.Scale(x_frame, from_=-1, to=1, length=250, command=lambda value: self.update_variable(self.x, value, preview_point))
        self.y_slider = ttkb.Scale(y_frame, from_=-1, to=1, length=250, command=lambda value: self.update_variable(self.y, value, preview_point))
        self.z_slider = ttkb.Scale(z_frame, from_=-1, to=1, length=250, command=lambda value: self.update_variable(self.z, value, preview_point))
        self.define_point_btn = ttkb.Button(self, text="Define Point")
        self.cancel_btn = ttkb.Button(self, text="Close")
        self.go_to_goal_btn = ttkb.Button(self, text="Go to goal")
        self.points_table = ttkb.tableview.Tableview(self, coldata=["Point_ID", "Coordinates"], rowdata=[], height=10)
        self.points_button_group = ButtonGroup(self, [("Define Point",),
                                                      ("Go to Goal",),
                                                      ("Cancel",)],
                                                     "default",
                                                     horizontal=True,
                                                     style="secondary.TButton")

        #table for all points
        #selectable points
        #go to selection

        first_row.pack(padx=10, pady=(50,20))
        self.label.pack(side='left')
        self.z_input.pack(side='right')
        self.y_input.pack(side='right')
        self.x_input.pack(side='right')
        self.xlabel.pack(side='left')
        self.x_slider.pack(pady=5)
        self.ylabel.pack(side='left')
        self.y_slider.pack(pady=5)
        self.zlabel.pack(side='left')
        self.z_slider.pack(pady=5)
        x_frame.pack()
        y_frame.pack()
        z_frame.pack()
        self.points_table.pack()
        self.points_button_group.pack()

    def update_variable(self, var, value, preview_point):
        rounded_value = round(float(value), 3)
        var.set(rounded_value)
        preview_point()

    
