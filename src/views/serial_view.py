import ttkbootstrap as ttkb
from tkinter.scrolledtext import *
from ttkbootstrap.constants import END, GROOVE
from src.views.components.button_group import ButtonGroup
from ttkbootstrap.dialogs.dialogs import Messagebox


class SerialView(ttkb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, borderwidth=2, relief=GROOVE)
        self.controller = controller
        self.header = ttkb.Label(self, text='Serial Communication', font=('bold', 12))
        self.ser_port = ttkb.StringVar()
        self.ports = []
        self.serial_window = ScrolledText(self, width=60, height=12, wrap=ttkb.WORD)
        self.serial_window.configure(state="disabled")
        self.serial_list_dropdown = ttkb.Combobox(self, textvariable=self.ser_port)
        self.serial_list_dropdown['values'] = self.ports 
        
        #Layout
        self.header.pack(pady=(5,5), anchor='nw')
        self.serial_list_dropdown.pack(pady=0, padx=5)
        self.serial_btns = ButtonGroup(self, [('Connect', self.controller.connect_to_port),
                                              ('Scan', self.controller.get_port_list),
                                              ('Clear', self.clear_window),
                                              ('Send Message', self.controller.send_serial_msg)
                                                ], container_style='default', style=None, horizontal=True)

        self.serial_btns.pack()
        self.serial_window.pack()

    def show_connected_msg(self):
        self.serial_window.configure(state="normal")
        self.serial_window.insert(END, f'Connected to serial device on port: {self.ser_port.get()}')
        self.serial_window.yview(END)
        self.serial_window.configure(state="disabled")

    def serial_connected(self):
        self.serial_btns.buttons['Connect'].configure(text="Disconnect", command=self.controller.disconnect)

    def new_msg(self, msg):
        print("Got a new message")
        print(msg)
        if len(msg) > 0:
            self.serial_window.configure(state="normal")
            self.serial_window.insert(END, msg + '\n')
            self.serial_window.yview(END)
            self.serial_window.configure(state="disabled")

    def clear_window(self):
        self.serial_window.configure(state='normal')
        self.serial_window.delete('1.0', ttkb.END)
        self.serial_window.configure(state='disabled')

    def serial_disconnected(self):
        self.serial_btns.buttons['Connect'].configure(text="Connect", command=self.controller.connect_to_port)
        self.serial_window.configure(state="normal")
        self.serial_window.delete(1.0, END)

    def update_dropdown(self):
        self.serial_list_dropdown['values'] = self.ports

    def error_msg(self, msg):
       Messagebox.ok(msg)


    def update(self):
        self.after(20, self.controller.update_serial_window)

