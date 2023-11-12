import ttkbootstrap as ttk

class JointConfig(ttk.Frame):
    def __init__(self, parent, label, val):
        super().__init__(parent)

        self.val = val

        self.label = ttk.Label(self, text=f'{label}: ', font=('bold', 12))
        self.label.pack(side='left', padx=10, pady=10)

        self.value = ttk.Label(self, textvariable=self.val, font=('normal',12))
        self.value.pack(pady=10)