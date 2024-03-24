from src.serial_service import SerialService
from ttkbootstrap.constants import *
from src.views.serial_view import SerialView

class SerialController:
    def __init__(self, root, parent):
        self.view = SerialView(parent, self)
        self.serial_service = SerialService(self)

    def show_view(self):
        self.get_port_list()
        self.view.pack_propagate(0)
        self.view.pack(anchor='nw', fill='both', expand=True, padx=0, pady=0)


    def kill_view(self):
        print("Closing the Serial communications")
        self.view.destroy()


    def get_port_list(self):
        ports = self.serial_service.get_ports()
        self.view.ports = ports
        self.view.update_dropdown()


    def connect_to_port(self, port):
        self.serial_service.connect(port)
        self.serial_kill_loop.clear()
        if self.serial_connection.is_open:
            self.view.after(50, self.update_serial_window)
            self.view.show_connected_msg()
            self.view.serial_connected()


    def update_serial_window(self):
        try:
            new_msg = self.serial_service.message_queue.get_nowait()
            self.view.new_msg(new_msg)
            self.view.after(20, self.update_serial_window)

        except Exception as e:
            if e:
                pass
            else:
                pass      
 

    def disconnect(self):
        self.serial_service.disconnect()
        #self.view.serial_disconnected()

    def on_close(self):
        self.serial_kill_loop.set()
        self.serial_thread.join()

