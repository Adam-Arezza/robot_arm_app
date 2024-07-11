import ttkbootstrap as ttkb


class GoalPointView(ttkb.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        first_row = ttkb.Frame(self)
        self.header = ttkb.Label(self,text="Goal Point Definition", font=('Helvetica', 12, 'bold'))
        self.label = ttkb.Label(first_row,text="XYZ: ", font=('Helvetica', 12, 'bold'))
        self.x = ttkb.StringVar()
        self.y = ttkb.StringVar()
        self.z = ttkb.StringVar()
        self.x_input = ttkb.Entry(first_row, textvariable=self.x)
        self.y_input = ttkb.Entry(first_row, textvariable=self.y)
        self.z_input = ttkb.Entry(first_row, textvariable=self.z)
        self.define_point_btn = ttkb.Button(self, text="Define Point")


        self.header.pack()
        first_row.pack(padx=20, pady=20)
        self.label.pack(side='left')
        self.z_input.pack(side='right')
        self.y_input.pack(side='right')
        self.x_input.pack(side='right')
        self.define_point_btn.pack()

    
  
