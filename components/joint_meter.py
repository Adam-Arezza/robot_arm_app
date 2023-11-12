import ttkbootstrap as ttk

class JointMeter(ttk.Frame):
    def __init__(self, parent, meter_val):
        super().__init__(parent)
        
        self.meter = ttk.Meter(self,
                               interactive=False,
                               amounttotal=180,
                               amountused=meter_val,
                               metersize=100)
        
        self.meter.pack()