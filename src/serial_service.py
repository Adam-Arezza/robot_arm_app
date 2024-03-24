import serial
from serial.tools import list_ports
import threading
from queue import Queue
import time


class SerialService:
    def __init__(self, controller):
        self.message_queue = Queue()
        self.port_list = [i.name for i in list_ports.comports()]
        self.serial_connection = None
        self.controller = controller
        self.serial_kill_loop = threading.Event()
        self.thread_running = False
        #self.after(50, self.controller.update_serial_window)


    def connect(self, port):
        try:
            self.serial_connection = serial.Serial(port=port, baudrate=115200, timeout=0.2)
            if not self.thread_running:
                self.thread = threading.Thread(target=self.get_serial_msg, daemon=True)
                self.serial_thread.start()
                self.thread_running = True
        
        except Exception as e:
            print(e)


    def get_ports(self):
        ports = [i.name for i in list_ports.comports()]
        return ports


    def get_serial_msg(self):
        while not self.serial_kill_loop.is_set():
            if self.serial_connection.inWaiting() > 0:
                data = self.serial_connection.readline().decode()
                self.message_queue.put(data)
                self.controller.update_serial_window()
            time.sleep(0.01)


    def disconnect(self):
        print("Closing serial port")
        self.serial_kill_loop.set()
        print("kill loop set")
        if self.serial_connection:
            self.serial_connection.close()
        print("connection closed")
        self.thread_running = False
        print("thread not running")
        #self.controller.disconnect()
        print("Serial port closed")



