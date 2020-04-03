import sys

from PyQt5 import QtGui
import mainwindow as UI_main
import newconnecthandler as NC_handler
import openconnecthandler as OC_handler
from PyQt5.QtWidgets import QApplication, QMainWindow
import serialprocess as mySerial
from PyQt5.QtWidgets import QMessageBox
import configutil as Config
from main import global_data as g_data
import binascii


class MyMainWindow(QMainWindow, UI_main.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.ser = mySerial.serialProcess()       #实例串口类

        self.cfgPar = Config.configParser()       #实例配置项类,界面同步部分配置项
        self.actionTime.setChecked(self.cfgPar.is_show_time())
        self.actionTag.setChecked(self.cfgPar.is_show_tag())
        self.actionFile.setChecked(self.cfgPar.is_show_level())
        g_data.rec_show['time'] = True if self.actionTime.isChecked() else False
        g_data.rec_show['tag'] = True if self.actionTime.isChecked() else False
        g_data.rec_show['level'] = True if self.actionTime.isChecked() else False

        # 子窗口需要为主窗口的成员变量，否则子窗口会一闪而过
        self.newConnect = NC_handler.MyNewConnect()#新连接的窗口
        self.openConnect = OC_handler.MyOpenConnect()#打开的窗口
        self.buildConnect()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        reply = QMessageBox.question(self, 'Serial Tool', "是否要退出程序？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.cfgPar.write_to_config()
            self.ser.port_close()
            self.destroy()
            a0.accept()
        else:
            a0.ignore()

    def buildConnect(self):
        self.buttonSend.clicked.connect(self.slot_SendMessage)

        self.actionNew.triggered.connect(self.slot_NewConnect)
        self.actionOpen.triggered.connect(self.slot_OpenConnect)

        self.actionDisconnect.triggered.connect(self.ser.port_close)
        self.actionRe_Connect.triggered.connect(self.ser.port_connect)

        self.actionTime.triggered.connect(self.slot_show_time)   #显示时间
        self.actionFile.triggered.connect(self.slot_show_level)  # 显示等级
        self.actionTag.triggered.connect(self.slot_show_tag)  # 显示标签

        self.actionIPC_parse.triggered.connect(self.slot_ipc_parser)
        self.ser.SerialSignal.connect(self.slot_Serial_emit)

    def slot_SendMessage(self):
        text = self.lineEditSend.currentText().strip()
        text_list = text.split(' ')
        if "" != text:
            if text_list[0] == 'filter':
                if text_list[1] in g_data.rec_filter:
                    print(text_list)
                    g_data.rec_filter[text_list[1]] = text_list[2:]
                    print(g_data.rec_filter[text_list[1]])
                elif text_list[1] == 'reset':
                    g_data.rec_filter = {'level': ['error', 'warn', 'info', 'debug'], 'tag': [], 'content': []}
            elif text_list[0] == 'config':
                if len(text_list) is 4:
                    self.cfgPar.set_config(text_list[1], text_list[2], text_list[3])
            else:
                if self.cfgPar.get_send_format() == 'hex':
                    send_list = []
                    while text != '':
                        try:
                            num = int(text[0:2], 16)
                        except ValueError:
                            QMessageBox.critical(self, 'wrong data', '请输入十六进制数据，以空格分开!')
                            return None
                        text = text[2:].strip()
                        send_list.append(num)
                    input_s = bytes(send_list)
                else:
                    input_s = (text + '\r\n').encode('utf-8')
                self.ser.port_send(input_s)
            self.textEditRecvive.insertPlainText(text + '\r\n')

    def slot_NewConnect(self):
        self.newConnect.set_PortList(self.ser.Com_List)
        self.newConnect.update_port_id(self.cfgPar.get_port_count())
        self.newConnect.NewConSignal.connect(self.slot_NewConnect_emit)
        self.newConnect.show()

    def slot_OpenConnect(self):
        self.openConnect.get_serial_list(self.cfgPar.get_serial_config_list())
        self.openConnect.OpenConSignal.connect(self.slot_OpenConnect_emit)
        self.openConnect.show()

    def slot_OpenConnect_emit(self, flag, dic):
        if flag == 0:  # connect
            self.ser.update_serial_info(dic)
            self.ser.port_connect()
            if self.ser.serial.isOpen():
                self.textEditRecvive.insertPlainText(dic['port'] + " is connected\r\n")
                self.actionRe_Connect.setEnabled(True)
            else:
                self.textEditRecvive.insertPlainText(dic['port'] + " can not be connected\r\n")
        else:
            pass
        self.openConnect.OpenConSignal.disconnect()

    def slot_NewConnect_emit(self, flag, dic):
        if flag == 0:  # connect
            self.cfgPar.add_serial_config(dic)
            self.ser.update_serial_info(dic)
            self.ser.port_connect()
            if self.ser.serial.isOpen():
                self.textEditRecvive.insertPlainText(dic['port'] + " is connected\r\n")
                self.actionDisconnect.setEnabled(True)
                self.actionRe_Connect.setEnabled(True)
        elif flag == 1:  # ok
            self.cfgPar.add_serial_config(dic)
            pass
        else:
            pass
        self.newConnect.NewConSignal.disconnect()

    def slot_Serial_emit(self, flag, data):
        if flag == 'receive':  # rec
            # hex显示
            if self.cfgPar.get_show_format() == 'hex':
                bytes_16 = binascii.b2a_hex(data)
                out_s = ''
                for i in range(0, len(data)):
                    out_s = out_s + '{:02X}'.format(bytes_16[i]) + ' '
                self.textEditRecvive.insertPlainText(out_s)
            else:
                self.textEditRecvive.insertPlainText(data)
            textCursor = self.textEditRecvive.textCursor()
            textCursor.movePosition(textCursor.End)
            self.textEditRecvive.setTextCursor(textCursor)
        elif flag == 'send':  # send
            pass
        else:
            pass

    def slot_show_time(self):
        value = True if self.actionTime.isChecked() else False
        g_data.rec_show['time'] = value
        self.cfgPar.set_config('showCfg', 'show_time', str(value))

    def slot_show_tag(self):
        value = True if self.actionTime.isChecked() else False
        g_data.rec_show['tag'] = value
        self.cfgPar.set_config('showCfg', 'show_tag', str(value))

    def slot_show_level(self):
        value = True if self.actionTime.isChecked() else False
        g_data.rec_show['level'] = value
        self.cfgPar.set_config('showCfg', 'show_level', str(value))
        pass

    def slot_ipc_parser(self):
        g_data.rec_filter = {'level': ['debug'], 'tag': ['ipc'], 'content': ['drv recv', 'drv send']}
        g_data.plug_tool['ipc'] = True

