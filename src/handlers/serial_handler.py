import threading
import time
import queue
from src.serial_service import SerialService
from ttkbootstrap.constants import *
from src.views.serial_view import SerialView


class SerialHandler:
    def __init__(self, serial_service, parent):
        self.serial_service = serial_service
        self.view = SerialView(parent, self)
        self.update_thread_running = False
        self.kill_update_thread = threading.Event() 
        self.get_port_list()


    def get_port_list(self):
        self.view.update_dropdown(self.serial_service.get_ports())


    def connect_to_port(self):
        port = self.view.ser_port.get()
        self.serial_service.connect(port)
        

    def add_serial_connection(self, port:str):
        self.view.show_connected_msg(port)
        self.view.serial_connected()
        self.start_update_thread()


    def start_update_thread(self):
        self.update_thread_running = True
        self.update_thread = threading.Thread(target=self.serial_data_update, daemon=True)
        self.update_thread.start()


    def serial_data_update(self):
        while self.update_thread_running:
            try:
                new_msg = self.serial_service.message_queue.get_nowait()
                if new_msg and len(new_msg) > 0:
                    if new_msg[0] != "<":
                        print("Invalid data format for received message")
                    else:
                        new_msg = new_msg.removeprefix("<")
                        new_msg = new_msg.replace(">", "")
                        print("data received, publishing new data event")
                        self.serial_service.publish_serial_event('new_data', new_msg)
            except queue.Empty:
                pass
            except Exception as e:
                if e:
                    print("Serial handler - Error updating window")
                    print(e)
            time.sleep(0.02)


    def update_serial_window_received(self, data):
        self.view.update_serial_window_received(data)


    def update_serial_window_sent(self, data):
        self.view.update_serial_window_sent(data)


    def remove_serial_connection(self,port):
        pass

    
    def disconnect(self):
        self.serial_service.disconnect()
        self.view.serial_disconnected()
        self.kill_update_thread.set()
        self.update_thread_running = False


    def on_close(self):
        self.kill_update_thread.set()
        self.serial_service.thread.join()

