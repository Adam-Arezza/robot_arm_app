import ttkbootstrap as ttkb
from tkinter.scrolledtext import *
from ttkbootstrap.constants import END, GROOVE
from src.views.components.button_group import ButtonGroup
from ttkbootstrap.dialogs.dialogs import Messagebox


class SerialView(ttkb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.name = 'serial_view'
        self.ser_port = ttkb.StringVar()
        self.serial_window = ScrolledText(self, width=60, height=40, wrap=ttkb.WORD)
        self.serial_window.configure(state="disabled", bg='black', fg='lime')
        self.inputs_frame = ttkb.Frame(self)
        self.serial_list_dropdown = ttkb.Combobox(self.inputs_frame, textvariable=self.ser_port, width=15)
        self.inputs_label = ttkb.Label(self.inputs_frame, text="Available ports: ")
        self.serial_btns = ButtonGroup(self.inputs_frame, [('Connect', self.controller.connect_to_port),
                                                           ('Scan', self.controller.get_port_list),
                                                           ('Clear', self.clear_window)
                                                           ], container_style='default', style=None, horizontal=True)
        #Layout
        self.inputs_label.pack(side='left')
        self.serial_list_dropdown.pack(pady=0, padx=5, side='left')
        self.serial_btns.pack()
        self.inputs_frame.pack(pady=20)
        self.serial_window.pack(padx=20, pady=20)


    def show_connected_msg(self, port:str):
        self.serial_window.configure(state="normal")
        self.serial_window.insert(END, f'Connected to serial device on port: {port}')
        self.serial_window.yview(END)
        self.serial_window.configure(state="disabled")


    def serial_connected(self):
        self.serial_btns.buttons['connect'].configure(text="Disconnect", command=self.controller.disconnect)


    def sending_message(self, msg:str):
        if len(msg) > 0:
            self.serial_window.configure(state="normal")
            self.serial_window.insert(END,f'Sending: {msg} \n')
            self.serial_window.yview(END)
            self.serial_window.configure(state="disabled")


    def update_serial_window_received(self, msg:str):
        if len(msg) > 0:
            self.serial_window.configure(state="normal")
            self.serial_window.insert(END,f'Received:  {msg} \n')
            self.serial_window.yview(END)
            self.serial_window.configure(state="disabled")


    def update_serial_window_sent(self, msg:str):
        if len(msg) > 0:
            self.serial_window.configure(state="normal")
            self.serial_window.insert(END,f'Sent:  {msg} \n')
            self.serial_window.yview(END)
            self.serial_window.configure(state="disabled")


    def clear_window(self):
        self.serial_window.configure(state='normal')
        self.serial_window.delete('1.0', ttkb.END)
        self.serial_window.configure(state='disabled')


    def serial_disconnected(self):
        self.serial_btns.buttons['connect'].configure(text="Connect", command=self.controller.connect_to_port)
        self.serial_window.configure(state="normal")
        self.serial_window.delete(1.0, END)


    def update_dropdown(self, port_list:list):
        self.serial_list_dropdown['values'] = port_list


    def error_msg(self, msg:str):
        Messagebox.ok(msg)

