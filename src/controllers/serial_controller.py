from src.serial_service import SerialService
from ttkbootstrap.constants import *
from src.views.serial_view import SerialView
import threading

class SerialController:
    def __init__(self, serial_service, parent):
        self.serial_service = serial_service
        self.view = SerialView(parent, self)
        self.joint_table = None


    def add_joint_table(self, joint_table):
        self.joint_table = joint_table


    def get_port_list(self):
        ports = self.serial_service.get_ports()
        self.view.ports = ports
        self.view.update_dropdown()


    def connect_to_port(self):
        port = self.view.ser_port.get()
        self.serial_service.connect(port)
        if self.serial_service.serial_connection.is_open:
            self.view.show_connected_msg()
            self.view.serial_connected()
        else:
            self.view.show_error_msg()


    #change to get_joint_table_values
    def get_joint_values(self):
        joint_values = self.joint_table.get_rows(selected=True)
        if len(joint_values) > 1:
            self.view.error_msg('Select only 1 joint configuration')
            return
        joint_values = joint_values[0].values
        joint_values = [str(i) for i in joint_values]
        return joint_values


    def send_serial_msg(self, joint_values=[]):
        j_vals = None
        if len(joint_values) == 0:
            j_vals = self.get_joint_values()
        else:
            j_vals = joint_values
        separator = ':'
        serial_msg = f'<{separator.join(j_vals)}>'.encode()
        print(serial_msg)
        if not self.serial_service.serial_connection:
            self.view.error_msg('There is no serial connection')
            return
        if not self.serial_service.serial_connection.is_open:
            self.serial_service.serial_connection.open()
            self.serial_service.send_serial_msg(serial_msg)
            self.view.sending_message(serial_msg)
        else:
            self.serial_service.send_serial_msg(serial_msg)
            self.view.sending_message(serial_msg)


    def update_serial_window(self, new_msg):
        try:
            self.view.new_msg(new_msg)
        except Exception as e:
            if e:
                print(e)
 

    def disconnect(self):
        self.serial_service.disconnect()
        self.view.serial_disconnected()


    def on_close(self):
        self.serial_kill_loop.set()
        self.serial_service.thread.join()

