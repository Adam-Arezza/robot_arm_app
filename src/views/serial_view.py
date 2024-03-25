import ttkbootstrap as ttkb
from tkinter.scrolledtext import *
from ttkbootstrap.constants import END, GROOVE


class SerialView(ttkb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, borderwidth=2, relief=GROOVE)
        self.controller = controller
        self.header = ttkb.Label(self, text='Serial Communication', font=('bold', 12))
        
        self.ser_port = ttkb.StringVar()
        self.ports = []
        self.serial_window = ScrolledText(self, width=60, height=8, wrap=ttkb.WORD)
        self.serial_window.configure(state="disabled")
        self.serial_list_dropdown = ttkb.Combobox(self, textvariable=self.ser_port)
        self.serial_list_dropdown['values'] = self.ports 
        self.connect_btn = ttkb.Button(self, 
                                       text='Connect', 
                                       command=self.controller.connect_to_port)
        self.scan_btn = ttkb.Button(self, 
                                    text='Scan Ports', 
                                    command=self.controller.get_port_list)

        #Layout
        self.header.pack(pady=(5,5), anchor='nw')
        self.serial_list_dropdown.pack(side='left', pady=0, padx=5)
        self.connect_btn.pack(side='left', padx=5)
        self.scan_btn.pack(side='left', padx=5)

    def show_connected_msg(self):
        self.serial_window.pack()
        self.view.serial_window.configure(state="normal")
        self.view.serial_window.insert(END, f'Connected to serial device on port: {self.ser_port.get()}')
        self.view.serial_window.yview(END)
        self.view.serial_window.configure(state="disabled")

    def serial_connected(self):
        #self.disconnect_btn = ttkb.Button(self, text='Disconnect', command=self.disconnect)
        #self.disconnect_btn.pack(padx=15)
        self.connect_btn.configure(text="Disconnect", command=self.controller.disconnect)
        self.clear_btn = ttkb.Button(self, text="Clear", command=self.clear_window)
        self.clear_btn.pack(side=ttkb.RIGHT)

    def new_msg(self, msg):
        self.serial_window.configure(state="normal")
        self.serial_window.insert(END, new_msg)
        self.serial_window.yview(END)
        self.serial_window.configure(state="disabled")

    def clear_window(self):
        self.serial_window.configure(state='normal')
        self.serial_window.delete('1.0', ttkb.END)
        self.serial_window.configure(state='disabled')

    def serial_disconnected(self):
        self.serial_window.pack_forget()
        self.serial_list_dropdown.pack(side='left')
        self.serial_btns.pack()
        self.connect_btn.configure(text="Connect", command=self.controller.connect_to_port)
        self.serial_window.configure(state="normal")
        self.serial_window.delete(1.0, END)

    def update_dropdown(self):
        self.serial_list_dropdown['values'] = self.ports
