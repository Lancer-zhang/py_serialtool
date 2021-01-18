import serial
# pip install pyserial
import serial.tools.list_ports
import threading
import time
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal


class serialProcess(QObject):
    SerialSignal = pyqtSignal(str, bytes)

    def __init__(self, parent=None):
        super(serialProcess, self).__init__(parent)
        self.serial = serial.Serial()
        self.Com_List = []
        self.port = 'COM1'
        self.baud = 9600
        self.dataBits = 8
        self.stopBits = 1
        self.parity = 'None'
        self.data_received = 0
        self.data_send = 0
        self.port_check()
        self.read_thread = readThread()

    def port_check(self):
        # 检测所有存在的串口，将信息存储在字典中
        port_list = list(serial.tools.list_ports.comports())
        for port in port_list:
            self.Com_List.append(port[0])
        print(self.Com_List)

    def update_serial_info(self, port_dict):
        if len(port_dict) > 0:
            self.serial.port = port_dict['port']
            self.serial.baudrate = int(port_dict['baud'])
            self.serial.bytesize = int(port_dict['data'])
            self.serial.stopbits = float(port_dict['stop'])
            self.serial.parity = str(port_dict['parity'])[0]

    def port_connect(self):
        try:
            if self.serial.port is not None and not self.serial.isOpen():

                self.serial.open()
                if self.serial.isOpen():
                    print(self.serial.port + " opened")
                    if not self.read_thread.alive:
                        print("1")
                        self.read_thread.start(self.port_receive)
                    else:
                        print("2")
                        self.read_thread.stop()
                        self.read_thread.start(self.port_receive)
            else:
                print("can not open")
        except Exception as e:
            print(e)
            return None

    def port_close(self):
        if self.serial.isOpen():
            self.read_thread.stop()
            print("close " + self.serial.port)
            try:
                self.serial.close()
            except:
                pass

    def port_send(self, data):
        if self.serial.isOpen():
            try:
                self.serial.write(data)
            except:
                pass
        else:
            pass

    def port_receive(self):
        while self.read_thread.alive and self.serial.isOpen():
            # self.read_thread.waiting()
            time.sleep(0.005)  # 1ms
            try:
                num = self.serial.inWaiting()
            except Exception as e:
                print(e)
             #   self.SerialSignal.emit('error', Null)
                return None
            data = self.serial.read(num)
            if len(data) > 0:
                self.SerialSignal.emit('receive', data)


class readThread:
    def __init__(self):
        self.thread_read = None
        self.alive = False
        self.waitEnd = None

    def waiting(self):
        if self.waitEnd is not None:
            self.waitEnd.wait()

    def pause(self):
        if self.waitEnd is not None:
            self.waitEnd.clear()

    def resume(self):
        if self.waitEnd is not None:
            self.waitEnd.set()

    def start(self, reader):
        self.waitEnd = threading.Event()
        self.alive = True
        self.thread_read = threading.Thread(target=reader)
        self.thread_read.setDaemon(1)
        self.thread_read.start()
        self.resume()
        return True

    def stop(self):
        self.alive = False
        self.resume()
        self.thread_read.join()
