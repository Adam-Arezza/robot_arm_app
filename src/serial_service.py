import serial
from serial.tools import list_ports
import threading
from queue import Queue
import time


class SerialService:
    def __init__(self, controller):
        self.message_queue = []
        self.port_list = [i.name for i in list_ports.comports()]
        self.serial_connection = None
        self.controller = controller
        self.serial_kill_loop = threading.Event()
        self.thread_running = False


    def connect(self, port):
        try:
            self.serial_connection = serial.Serial(port=port, baudrate=115200, timeout=0.1)
            self.serial_kill_loop.clear()
            if self.serial_connection and self.serial_connection.isOpen():
                print(f"Connected to {port}")
                if not self.thread_running:
                    self.thread = threading.Thread(target=self.get_serial_msg, daemon=True)
                    self.thread.start()
                    self.thread_running = True
        
        except serial.SerialException as e:
            print(e)


    def get_ports(self):
        ports = [i.name for i in list_ports.comports()]
        return ports


    def get_serial_msg(self):
        print("Started thread")
        if not self.serial_connection.is_open:
            self.serial_connection.open()
        while self.thread_running:
            if self.serial_connection.is_open:
                try:
                    data = self.serial_connection.readline().decode()
                    #print(data)
                    if len(data) > 0:
                        self.message_queue.append(data)
                    self.serial_connection.reset_input_buffer()
                    self.controller.update_serial_window()
                except Exception as e:
                    print(f"There was an error: {e}")
            time.sleep(0.1)


    def send_serial_msg(self, msg):
        print("Sending serial message now")
        if self.serial_connection:
            self.serial_connection.write(msg)
            #response = self.serial_connection.readline().decode()
            #self.message_queue.put(response)
            self.serial_connection.reset_input_buffer()


    def disconnect(self):
        print("Closing serial port")
        self.serial_kill_loop.set()
        print("kill loop set")
        if self.serial_connection.is_open:
            self.serial_connection.close()
        print("connection closed")
        self.thread_running = False
        print("thread not running")
        print("Serial port closed")



