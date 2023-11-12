import ttkbootstrap as ttk
import serial
from serial.tools import list_ports

class SerialConnector(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style='secondary.TFrame')

        self.header = ttk.Label(self, text='Serial Ports:', font=('bold', 12), style='secondary.inverse')
        self.header.pack(pady=(40,5))

        self.ser_port = ttk.StringVar()
        self.port_list = [i.name for i in list_ports.comports()]
        self.serial_list_dropdown = ttk.Combobox(self, textvariable=self.ser_port)
        self.serial_list_dropdown['values'] = self.port_list 

        self.serial_list_dropdown.pack()

        self.connect_btn = ttk.Button(self, text='Connect', command=self.connect_to_port)
        self.connect_btn.pack(pady=15)
        # self.serial_connection
        
    def connect_to_port(self):
        print(f'Connecting to port {self.ser_port.get()}')
        # self.serial_connection = serial.Serial(port=self.ser_port, baudrate=115200)