import sys

from PyQt5.QtCore import pyqtSignal

import openconnect as UI_oc
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem


class MyOpenConnect(QDialog, UI_oc.Ui_Dialog):
    OpenConSignal = pyqtSignal(int, dict)

    def __init__(self, parent=None):
        super(MyOpenConnect, self).__init__(parent)
        self.setupUi(self)
        self.ports_list = []
        self.current_port = {}
        self.tableWidget.clicked.connect(self.slot_select_port)
        self.pushButtonConnect.clicked.connect(self.slot_connect)
        self.pushButtonClose.clicked.connect(self.destroy)
        self.pushButtonNew.clicked.connect(self.slot_new_connect)
        self.pushButtonDelete.clicked.connect(self.slot_delete_connect)
        self.pushButtonTrait.clicked.connect(self.slot_show_connect)
        self.pushButtonClose.clicked.connect(self.slot_close_window)

    def get_serial_list(self, portList):
        self.ports_list.clear()
        self.ports_list = portList
        row = self.tableWidget.rowCount()
        while row > 0:
            row = row - 1
            self.tableWidget.removeRow(row)
        row = self.tableWidget.rowCount()
        for port in portList:
            self.tableWidget.insertRow(row)
            newItem = QTableWidgetItem(port['name'])
            self.tableWidget.setItem(row, 0, newItem)
            newItem = QTableWidgetItem(port['port'])
            self.tableWidget.setItem(row, 1, newItem)
            newItem = QTableWidgetItem('Serial Port')
            self.tableWidget.setItem(row, 2, newItem)
            row = row + 1

    def slot_select_port(self):
        row = self.tableWidget.currentRow()
        name = self.tableWidget.item(row, 0).text()
        for port in self.ports_list:
            if port['name'] == name:
                self.current_port = port

    def slot_connect(self):
        if len(self.current_port) > 0:
            self.OpenConSignal.emit(0, self.current_port)
            self.destroy()

    def slot_new_connect(self):
        self.OpenConSignal.emit(1, self.current_port)
        self.destroy()

    def slot_delete_connect(self):
        if len(self.current_port) > 0:
            self.OpenConSignal.emit(2, self.current_port)
            self.ports_list.remove(self.current_port)
            self.tableWidget.removeRow(self.tableWidget.currentRow())

    def slot_show_connect(self):
        pass

    def slot_close_window(self):
        self.destroy()

