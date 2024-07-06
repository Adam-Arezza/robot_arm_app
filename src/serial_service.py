import serial
import time
import threading
import time
import queue
from serial.tools import list_ports


class SerialService:
    def __init__(self):
        self.response_queue = queue.Queue()
        self.command_queue = queue.Queue()
        self.slider_command_queue = queue.Queue()
        self.port_list = [i.name for i in list_ports.comports()]
        self.serial_connection = None
        self.serial_kill_loop = threading.Event()
        self.thread_running = False
        self.slider_thread_running = False
        self.subscribers = {}
        


    def connect(self, port:str):
        try:
            self.serial_connection = serial.Serial(port=port, baudrate=115200, timeout=0.05)
            self.serial_kill_loop.clear()
            if self.serial_connection and self.serial_connection.isOpen():
                self.publish_serial_event('connected', port)
                if not self.thread_running:
                    self.start_thread()
                    self.start_slider_thread()
        except serial.SerialException as e:
            self.log_msg(f"Error during serial connection: {e}", "ERROR")
            print(e)


    def start_thread(self):
        self.thread = threading.Thread(target=self.get_serial_msg, daemon=True)
        self.thread_running = True 
        self.thread.start()


    def start_slider_thread(self):
        self.slider_thread = threading.Thread(target=self.check_slider_command_queue, daemon=True)
        self.slider_thread_running = True
        self.slider_thread.start()


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
        while self.thread_running:
            try:
                data = self.serial_connection.readline().decode()
                if len(data) > 0:
                    self.response_queue.put_nowait(data)
                    self.broadcast_responses()
            except Exception as e:
                self.log_msg(f"Serial Service error: {e}", "ERROR")
                print(f"Serial Service error: {e}")


    def check_slider_command_queue(self):
        while self.slider_thread_running:
            try:
                new_command = self.slider_command_queue.get_nowait()
                new_command = self.format_msg(new_command)
                self.send_serial_msg(new_command)
            except queue.Empty:
                pass
            except Exception as e:
                self.log_msg(f"Error processing slider commands: {e}", "ERROR")
                print(f"Error processing slider commands: {e}")
            time.sleep(0.05)


    def send_serial_msg(self, msg:str):
        if self.serial_connection:
            try:
                self.serial_connection.write(msg)
                self.publish_serial_event('log', f"sent to robot controller -> {msg}")
            except Exception as e:
                self.log_msg(f"Error sending serial data: {e}", "ERROR")
                print("Error writing serial message:")
                print(e)


    def add_slider_command(self, command:list):
        self.slider_command_queue.put_nowait(command)


    def start_trajectory_queue(self, commands:list):
        for command in commands:
            self.command_queue.put(command, block=True)
        self.next_command()


    def next_command(self):
        command = self.command_queue.get_nowait()
        formatted_command = self.format_msg(command)
        print(f"The next command is: {command}")
        self.publish_serial_event('new_target', command)
        self.log_msg(f"New target -> {command}", "INFO")
        self.send_serial_msg(formatted_command)


    def format_msg(self, msg_data:list):
        string_arr = [str(i) for i in msg_data]
        separator = ':'
        result = f'<{separator.join(string_arr)}>'.encode()
        return result


    def broadcast_responses(self):
        if self.response_queue.qsize() > 0:
            try:
                new_msg = self.response_queue.get_nowait()
                if new_msg and len(new_msg) > 0:
                    if new_msg[0] != "<":
                        pass
                    else:
                        new_msg = new_msg.removeprefix("<")
                        new_msg = new_msg.replace(">", "")
                        self.log_msg(f"New data received -> {new_msg}", "INFO")
            except queue.Empty:
                pass
            except Exception as e:
                if e:
                    self.log_msg(f"Serial handler -> {e}", "ERROR")
                    print(f"Serial handler -> {e}")
                    print(e)


    def disconnect(self):
        print("Closing serial port")
        self.serial_kill_loop.set()
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            self.serial_connection = None
        print("connection closed")
        self.thread_running = False
        self.slider_thread_running = False
        self.publish_serial_event('disconnected', '')
        print("thread not running")
        print("Serial port closed")


    def log_msg(self, msg:str, log_type:str):
        self.publish_serial_event('log', [msg, log_type])
