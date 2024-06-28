from src.serial_service import SerialService
from ttkbootstrap.constants import *
from src.views.serial_view import SerialView


class SerialHandler:
    def __init__(self, root,  serial_service, parent):
        self.root = root
        self.serial_service = serial_service
        self.view = SerialView(parent, self)
        self.get_port_list()


    def get_port_list(self):
        self.view.update_dropdown(self.serial_service.get_ports())


    def connect_to_port(self):
        port = self.view.ser_port.get()
        self.serial_service.connect(port)
        

    def add_serial_connection(self, port:str):
        self.view.show_connected_msg(port)
        self.view.serial_connected()

   
    def update_serial_window_received(self, data):
        self.view.update_serial_window_received(data)


    def update_serial_window_sent(self, data):
        self.view.update_serial_window_sent(data)


    def remove_serial_connection(self,port):
        pass


    def log_message(self, msg):
        self.view.update_serial_log(msg)
    

    def disconnect(self):
        self.serial_service.disconnect()
        self.view.serial_disconnected()
        self.kill_update_thread.set()
        self.update_thread_running = False


    def on_close(self):
        self.kill_update_thread.set()
        self.serial_service.thread.join()

