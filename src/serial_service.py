import serial
import time
import threading
import time
import queue
from serial.tools import list_ports


class SerialService:
    def __init__(self):
        self.command_queue = queue.Queue()
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
                self.publish_serial_event('connected', port)
                if not self.thread_running:
                    self.start_thread()
        except serial.SerialException as e:
            self.log_msg(f"Error during serial connection: {e}", "ERROR")
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


    def publish_serial_event(self, event:str, data:str):
        for fn in self.subscribers[event]:
            fn(data)


    def get_serial_msg(self):
        try:
            while self.thread_running:
                try:
                    data = self.serial_connection.readline().decode(errors="ignore").strip()
                    if data and len(data) > 0 and data[0] == "<":
                        self.broadcast_response(data)
                    else:
                        print(".", end="", flush=True)
                except Exception as e:
                        self.log_msg(f"Serial Service error: {e}", "ERROR")
                        print(f"Serial Service error: {e}")
        except Exception as e:
            print(f"Serial read error: ", e)


    def send_serial_msg(self, msg:str):
        if self.serial_connection:
            try:
                self.serial_connection.write(msg)
                self.serial_connection.flush()
                self.publish_serial_event('log', f"sent to robot controller -> {msg}")
            except Exception as e:
                self.log_msg(f"Error sending serial data: {e}", "ERROR")
                print("Error writing serial message:")
                print(e)


    def start_trajectory_queue(self, commands:list):
        for command in commands:
            self.command_queue.put(command, block=False)
        self.next_command()


    def next_command(self):
        command = self.command_queue.get_nowait()
        formatted_command = self.format_msg(command)
        print(f"The next command is: {command}")
        print(f"The command queue has: {self.command_queue.qsize()} tasks left.")
        self.publish_serial_event('new_target', command)
        self.log_msg(f"New target -> {command}", "INFO")
        self.send_serial_msg(formatted_command)


    def format_msg(self, msg_data:list):
        string_arr = [str(i) for i in msg_data]
        separator = ':'
        result = f'<{separator.join(string_arr)}>'.encode()
        return result


    def broadcast_response(self, new_msg):
        print(f"data received: {new_msg}")
        try:
            if new_msg and len(new_msg) > 0:
               if new_msg[0] != "<":
                   print("invalid message from robot controller")
                   print(new_msg)
                   pass
               else:
                   new_msg = new_msg.removeprefix("<")
                   new_msg = new_msg.replace(">", "")
                   self.publish_serial_event('new_data', new_msg)
                   self.log_msg(f"New data received -> {new_msg}", "INFO")
        except Exception as e:
           self.log_msg(f"Serial service -> {e}", "ERROR")
           print(f"Serial service -> {e}")
           print(e)


    def disconnect(self, port=None):
        print("Closing serial port")
        self.serial_kill_loop.set()
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            self.serial_connection = None
        self.thread_running = False
        self.slider_thread_running = False
        if port:
            self.log_msg(f"Disconnected from device on port: {port}", "INFO")


    def log_msg(self, msg:str, log_type:str):
        self.publish_serial_event('log', [msg, log_type])
