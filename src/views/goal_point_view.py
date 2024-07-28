import ttkbootstrap as ttkb


class GoalPointView(ttkb.Frame):
    def __init__(self, parent, preview_point):
        super().__init__(parent)
        first_row = ttkb.Frame(self)
        x_frame = ttkb.Frame(self)
        y_frame = ttkb.Frame(self)
        z_frame = ttkb.Frame(self)

        self.header = ttkb.Label(self,text="Goal Point Definition", font=('Helvetica', 12, 'bold'))
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
        self.x_slider = ttkb.Scale(x_frame, from_=-1, to=1, length=250, variable=self.x, command=preview_point)
        self.y_slider = ttkb.Scale(y_frame, from_=-1, to=1, length=250, variable=self.y, command=preview_point)
        self.z_slider = ttkb.Scale(z_frame, from_=-1, to=1, length=250, variable=self.z, command=preview_point)
        self.define_point_btn = ttkb.Button(self, text="Define Point")
        self.cancel_btn = ttkb.Button(self, text="Close")


        self.header.pack()
        first_row.pack(padx=20, pady=20)
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
        self.define_point_btn.pack(anchor='e', side='left', padx=5, pady=10)
        self.cancel_btn.pack(anchor='w', pady=10)

    
  
