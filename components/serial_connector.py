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
        self.scan_btn = ttk.Button(self, text='Scan Ports', command=self.scan_for_ports)
        self.scan_btn.pack(side='right')
        self.serial_kill_loop = threading.Event()
        self.thread_running = False
        self.serial_window = ScrolledText(self, width=60, height=8, wrap=ttk.WORD)
        self.serial_window.configure(state="disabled")
        self.after(50, self.update_serial_window)

    def connect_to_port(self):
        self.serial_connection = serial.Serial(port=self.ser_port.get(), baudrate=115200, timeout=0.25) 
        self.serial_kill_loop.clear()
        if self.serial_connection.is_open:
            self.parent.add_serial_connection(self.serial_connection)
            self.connect_btn.pack_forget()
            self.serial_list_dropdown.pack_forget()
            self.serial_window.pack(after=self.header, anchor='nw')
            self.serial_window.configure(state="normal")
            self.serial_window.insert(END, f'Connected to serial device on port: {self.ser_port.get()}')
            self.serial_window.yview(END)
            self.serial_window.configure(state="disabled")
            self.disconnect_btn = ttk.Button(self, text='Disconnect', command=self.disconnect)
            self.disconnect_btn.pack(padx=15)
            if not self.thread_running:
                self.serial_thread = threading.Thread(target=self.get_serial_msg, daemon=True)
                self.serial_thread.start()
                self.thread_running = True

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

    def disconnect(self):
        self.serial_kill_loop.set()
        self.serial_connection.close()
        self.serial_window.pack_forget()
        self.serial_list_dropdown.pack(side='left')
        self.connect_btn.pack(padx=15)
        self.disconnect_btn.pack_forget()
        self.serial_window.configure(state="normal")
        self.serial_window.delete(1.0, END)
        self.parent.serial_command_btn.pack_forget()
        self.thread_running = False

    def on_close(self):
        self.serial_kill_loop.set()
        self.serial_thread.join()

    def scan_for_ports(self):
        self.port_list = [i.name for i in list_ports.comports()]
        self.serial_list_dropdown['values'] = self.port_list 

