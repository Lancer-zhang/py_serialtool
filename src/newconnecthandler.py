import sys

from PyQt5.QtCore import pyqtSignal
import newconnect as UI_nc
from PyQt5.QtWidgets import QDialog


class MyNewConnect(QDialog, UI_nc.Ui_newConnect):
    NewConSignal = pyqtSignal(int, dict)

    def __init__(self, parent=None):
        super(MyNewConnect, self).__init__(parent)
        self.setupUi(self)
        self.serial_dict = {}
        self.lineEditName.setText("NewConnect")
        self.pushButtonConnect.clicked.connect(self.slot_connect)
        self.pushButtonOK.clicked.connect(self.slot_confirm)
        self.pushButtonCancel.clicked.connect(self.slot_cancel)
        self.current_id = 0

    def slot_connect(self):
        self.serial_dict['name'] = self.lineEditName.text()
        self.serial_dict['port'] = self.comboBoxPort.currentText()
        self.serial_dict['baud'] = self.comboBoxBaud.currentText()
        self.serial_dict['data'] = self.comboBoxData.currentText()
        self.serial_dict['stop'] = self.comboBoxStop.currentText()
        self.serial_dict['parity'] = self.comboBoxCheck.currentText()
        self.serial_dict['_id'] = self.current_id
        self.NewConSignal.emit(0, self.serial_dict)
        self.destroy()

    def slot_confirm(self):
        self.serial_dict['name'] = self.lineEditName.text()
        self.serial_dict['port'] = self.comboBoxPort.currentText()
        self.serial_dict['baud'] = int(self.comboBoxBaud.currentText())
        self.serial_dict['data'] = int(self.comboBoxData.currentText())
        self.serial_dict['stop'] = float(self.comboBoxStop.currentText())
        self.serial_dict['parity'] = self.comboBoxCheck.currentText()
        self.serial_dict['_id'] = self.current_id
        self.NewConSignal.emit(1, self.serial_dict)
        self.destroy()
        pass

    def slot_cancel(self):
        self.destroy()
        pass

    def set_PortList(self, ports):
        for port in ports:
            self.comboBoxPort.addItem(port)
        if len(ports) == 0:
            print('no com')

    def update_port_id(self, args):
        self.current_id = args
        self.lineEditName.setText("NewConnect(" + str(self.current_id) + ')')
