from src.serial_service import SerialService
from ttkbootstrap.constants import *
from src.views.serial_view import SerialView
import threading

class SerialController:
    def __init__(self):
        #self.root = root
        #self.view = SerialView(parent, self)
        #self.serial_service = SerialService(self)
        #self.joint_table = joint_table
        print("initialized serial controller")


    def add_view(self, view):
        self.view = view

    def show_view(self):
        self.get_port_list()
        #self.view.pack_propagate(0)
        #self.view.pack(anchor='nw', fill='both', expand=True, padx=0, pady=0)
        #self.view.pack(anchor='nw', side='left', fill='both', expand=True)
        #self.view.grid(column=1, row=0, sticky='nsew')

    def kill_view(self):
        print("Closing the Serial communications")
        self.view.destroy()


    def get_port_list(self):
        ports = self.serial_service.get_ports()
        self.view.ports = ports
        self.view.update_dropdown()


    def connect_to_port(self):
        port = self.view.ser_port.get()
        self.serial_service.connect(port)
        #self.serial_service.serial_kill_loop.clear()
        if self.serial_service.serial_connection.is_open:
            self.view.after(50, self.update_serial_window)
            self.view.show_connected_msg()
            self.view.serial_connected()

    def send_serial_msg(self):
        joint_values = self.joint_table.get_rows(selected=True)
        if len(joint_values) > 1:
            self.view.error_msg('Select only 1 joint configuration')
            return
        joint_values = joint_values[0].values
        joint_values = [str(i) for i in joint_values]
        separator = ':'
        serial_msg = f'<{separator.join(joint_values)}>'.encode()
        print(serial_msg)
        if not self.serial_service.serial_connection:
            self.view.error_msg('There is no serial connection')
            return
        if not self.serial_service.serial_connection.is_open:
            self.serial_service.serial_connection.open()
            self.serial_service.send_serial_msg(serial_msg)
        else:
            self.serial_service.send_serial_msg(serial_msg)


    def update_serial_window(self):
        try:
            if len(self.serial_service.message_queue) > 0:
                new_msg = self.serial_service.message_queue.pop(0)
                self.view.new_msg(new_msg)
                self.view.update()
        except Exception as e:
            if e:
                print(e)
 

    def disconnect(self):
        self.serial_service.disconnect()
        self.view.serial_disconnected()

    def on_close(self):
        self.serial_kill_loop.set()
        self.serial_service.thread.join()

