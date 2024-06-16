import ttkbootstrap as ttkb
from ttkbootstrap import BooleanVar, StringVar
from src.views.slider_controls_view import SliderControls

class ControlsView(ttkb.Frame):
    def __init__(self,parent, cb, links):
        super().__init__(parent)
        self.name = 'controls_view'
        self.mode_value = BooleanVar(value=False)
        self.mode_string = StringVar(value='Offline')
        self.slider_controls = None
        self.check_btn_frame = ttkb.Frame(self, style='default')
        self.toggle_label = ttkb.Label(self.check_btn_frame, 
                                       textvariable=self.mode_string, 
                                       bootstyle='default',
                                       font=('Helvetica',10,'bold'))

        self.toggle_mode_switch = ttkb.Checkbutton(self.check_btn_frame,
                                                   onvalue=True,
                                                   offvalue=False,
                                                   variable=self.mode_value,
                                                   bootstyle='default')

        self.reset_btn = ttkb.Button(self.check_btn_frame, 
                                     text="Reset",
                                     style='secondary.TButton')
        self.toggle_label.pack(side='left')
        self.toggle_mode_switch.pack(side='left', padx=10, pady=5)
        self.check_btn_frame.pack(pady=20)
        self.reset_btn.pack()
        self.add_sliders(cb,links)


    def add_sliders(self, cb, links:list):
        if self.slider_controls:
            self.slider_controls.destroy()
        self.slider_controls = SliderControls(self, cb, links)
        self.slider_controls.pack(padx=(0,25), pady=15, expand=True, fill='both')

