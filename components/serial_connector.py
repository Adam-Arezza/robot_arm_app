import ttkbootstrap as ttk
import serial
from serial.tools import list_ports
#from ttkbootstrap.scrolled import ScrolledText
import threading
from queue import Queue
import time
from tkinter.scrolledtext import *
from tkinter.constants import END

class SerialConnector(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style='default')
        self.parent = parent
        self.header = ttk.Label(self, text='Serial Ports:', font=('bold', 12))
        self.header.pack(pady=(40,5), anchor='nw')
        self.message_queue = Queue()

        self.ser_port = ttk.StringVar()
        self.port_list = [i.name for i in list_ports.comports()]
        self.serial_list_dropdown = ttk.Combobox(self, textvariable=self.ser_port)
        self.serial_list_dropdown['values'] = self.port_list 

        self.serial_list_dropdown.pack(side='left')

        self.connect_btn = ttk.Button(self, text='Connect', command=self.connect_to_port)
        self.connect_btn.pack(padx=15)
        self.serial_connection = None
        self.serial_kill_loop = threading.Event()
        self.after(50, self.update_serial_window)

    def connect_to_port(self):
        self.serial_connection = serial.Serial(port=self.ser_port.get(), baudrate=115200, timeout=0.25) 
        if self.serial_connection.is_open:
            self.parent.add_serial_connection(self.serial_connection)
            self.connect_btn.destroy()
            self.serial_list_dropdown.destroy()
            self.serial_thread = threading.Thread(target=self.get_serial_msg, daemon=True)
            self.serial_thread.start()
            self.serial_window = ScrolledText(self, width=60, height=20)
            self.serial_window.pack(after=self.header, anchor='nw')
            self.serial_window.insert(END, f'Connected to serial device on port: {self.ser_port.get()}')
            self.serial_window.yview(END)
            self.serial_window.configure(state="disabled")

    def get_serial_msg(self):
        while not self.serial_kill_loop.is_set():
            if self.serial_connection.inWaiting() > 0:
                data = self.serial_connection.readline().decode()
                self.message_queue.put(data)
            time.sleep(0.1)

    def update_serial_window(self):
        try:
            new_msg = self.message_queue.get_nowait()
            self.serial_window.configure(state="normal")
            self.serial_window.insert(END, new_msg)
            self.serial_window.yview(END)
            self.serial_window.configure(state="disabled")
        except Exception as e:
            if e:
                #new_msg_label = ttk.Text(text=f'{e}', style='warn.inversed')
                #new_msg_label.pack(anchor='nw')
                pass
            else:
                pass
        self.after(20, self.update_serial_window)

    def on_close(self):
        self.serial_kill_loop.set()
        self.serial_thread.join()
