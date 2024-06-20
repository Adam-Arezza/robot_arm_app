import ttkbootstrap as ttkb
import tkinter.filedialog as fd


class PoseGenerator(ttkb.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        first_row = ttkb.Frame(self)
        second_row = ttkb.Frame(self)
        self.header = ttkb.Label(self,text="Pose Generator", font=('Helvetica', 12, 'bold'))
        self.pose_number_label = ttkb.Label(first_row,text="Number of poses: ", font=('Helvetica', 12, 'bold'))
        self.pose_number_input = ttkb.Entry(first_row)
        self.save_location = ttkb.StringVar()
        self.save_location_entry = ttkb.Entry(second_row)
        self.save_location_btn = ttkb.Button(second_row,text="save location", command=self.open_file_dialog)
        self.show_poses = ttkb.BooleanVar(value=False)
        self.show_poses_checkbox = ttkb.Checkbutton(self,variable=self.show_poses)
        self.generate_btn = ttkb.Button(self,text="Generate Poses")

        self.header.pack()
        first_row.pack(padx=20, pady=20)
        second_row.pack(padx=20, pady=20)
        self.pose_number_label.pack(side='left')
        self.pose_number_input.pack(side='right')
        self.save_location_btn.pack(side='left')
        self.save_location_entry.pack(side='right')
        self.generate_btn.pack()
    
    def open_file_dialog(self):
        self.save_location.set(fd.askdirectory())
        self.save_location_entry.insert(0,self.save_location.get())


