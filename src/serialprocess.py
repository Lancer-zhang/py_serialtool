import serial
# pip install pyserial
import serial.tools.list_ports
import threading
import time
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer, QObject
from PyQt5.QtCore import pyqtSignal
from receivehandler import receiveHandler


class serialProcess(QObject):
    SerialSignal = pyqtSignal(str, str)

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
        # 定时器接收数据
        # self.timer_rec = QTimer()
        # self.timer_rec.timeout.connect(self.port_receive)
        self.read_thread = readThread()
        self.rec = receiveHandler()

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
            if self.serial is not None and not self.serial.isOpen():
                print("open " + self.serial.port)
                self.serial.open()
                if self.serial.isOpen():
                    self.read_thread.start(self.port_receive)

        except:
            print("can not open " + self.serial.port)
            return None
        # 打开串口接收定时器，周期为2ms

    # self.timer_rec.start(2)

    def port_close(self):
        if self.serial.isOpen():
            #   self.timer_rec.stop()
            self.read_thread.stop()
            #   self.SerialSignal.disconnect()
            # self.timer_send.stop()
            try:
                self.serial.close()
            except:
                pass

    def port_send(self, data):
        if self.serial.isOpen():
            self.serial.write(data)
        else:
            pass

    def port_receive(self):
        while self.read_thread.alive:
            self.read_thread.waiting()
            time.sleep(0.05)
            try:
                num = self.serial.inWaiting()
            except:
                self.port_close()
                return None
            data = self.serial.read(num)
            num = self.serial.inWaiting()
            if len(data) > 1 and num == 0:
                self.SerialSignal.emit('receive', self.rec.rec_str_parse(data))
        print('stop-------\r\n')


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
