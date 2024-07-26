import ttkbootstrap as ttkb


class GoalPointView(ttkb.Frame):
    def __init__(self, parent, preview_point):
        super().__init__(parent)
        first_row = ttkb.Frame(self)
        self.header = ttkb.Label(self,text="Goal Point Definition", font=('Helvetica', 12, 'bold'))
        self.label = ttkb.Label(first_row,text="XYZ: ", font=('Helvetica', 12, 'bold'))
        self.x = ttkb.StringVar(value=0)
        self.y = ttkb.StringVar(value=0)
        self.z = ttkb.StringVar(value=0)
        self.x_input = ttkb.Entry(first_row, textvariable=self.x)
        self.y_input = ttkb.Entry(first_row, textvariable=self.y)
        self.z_input = ttkb.Entry(first_row, textvariable=self.z)

        self.x_slider = ttkb.Scale(self, from_=-1, to=1, length=100, variable=self.x, command=preview_point)
        self.y_slider = ttkb.Scale(self, from_=-1, to=1, length=100, variable=self.y, command=preview_point)
        self.z_slider = ttkb.Scale(self, from_=-1, to=1, length=100, variable=self.z, command=preview_point)
        self.define_point_btn = ttkb.Button(self, text="Define Point")


        self.header.pack()
        first_row.pack(padx=20, pady=20)
        self.label.pack(side='left')
        self.z_input.pack(side='right')
        self.y_input.pack(side='right')
        self.x_input.pack(side='right')
        self.x_slider.pack()
        self.y_slider.pack()
        self.z_slider.pack()
        self.define_point_btn.pack()

    
  
