import serial
import threading
import time
from serial.tools import list_ports
from queue import Queue
from typing import Callable


class SerialService:
    def __init__(self):
        self.message_queue = Queue()
        self.port_list = [i.name for i in list_ports.comports()]
        self.serial_connection = None
        self.serial_kill_loop = threading.Event()
        self.thread_running = False
        self.subscribers = {}


    def connect(self, port:str):
        try:
            self.serial_connection = serial.Serial(port=port, baudrate=115200, timeout=0.1)
            self.serial_kill_loop.clear()
            if self.serial_connection and self.serial_connection.isOpen():
                print(f"Connected to {port}")
                self.publish_serial_event('connected', port)
                if not self.thread_running:
                    self.start_thread()
        except serial.SerialException as e:
            print(e)


    def start_thread(self):
        self.thread = threading.Thread(target=self.get_serial_msg, daemon=True)
        self.thread_running = True 
        self.thread.start()


    def get_ports(self) -> list:
        self.port_list = [i.name for i in list_ports.comports()]
        return self.port_list


    def add_subscriber(self, e:str, fn):
        if not e in self.subscribers:
            self.subscribers[e] = []
        self.subscribers[e].append(fn)


    def publish_serial_event(self,e:str,d:str):
        for fn in self.subscribers[e]:
            fn(d)


    def get_serial_msg(self):
        while self.thread_running:
            try:
                data = self.serial_connection.readline().decode()
                if len(data) > 0:
                    self.message_queue.put_nowait(data)
            except Exception as e:
                print(f"Serial Service error: {e}")
            time.sleep(0.02)


    def send_serial_msg(self, msg:str):
        if self.serial_connection:
            self.serial_connection.write(msg)
            self.serial_connection.reset_input_buffer()


    def disconnect(self):
        print("Closing serial port")
        self.serial_kill_loop.set()
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            self.serial_connection = None
            self.publish_serial_event('disconnected', '')
        print("connection closed")
        self.thread_running = False
        print("thread not running")
        print("Serial port closed")

