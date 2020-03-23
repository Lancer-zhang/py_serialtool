import sys

from PyQt5 import QtGui
import mainwindow as UI_main
import newconnecthandler as NC_handler
import openconnecthandler as OC_handler
from PyQt5.QtWidgets import QApplication, QMainWindow
import serialprocess as mySerial
from PyQt5.QtWidgets import QMessageBox
import configutil as Config
import receivehandler as acHandler
from main import global_data as g_data


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
        self.actionBy.triggered.connect(self.slot_filter_by_tag)  # 根据标签筛选
        self.actionBy_level.triggered.connect(self.slot_filter_by_level)  # 根据等级筛选

        self.actionIPC_parse.triggered.connect(self.slot_ipc_parser)
        self.ser.SerialSignal.connect(self.slot_Serial_emit)

    def slot_SendMessage(self):
        text = self.lineEditSend.currentText().strip()
        if "" != text:
            if text.split(' ')[0] == 'filter':
                pass
            elif text.split(' ')[0] == 'config':
                cfg_list = text.split(' ')
                self.cfgPar.set_config(cfg_list[1], cfg_list[2], cfg_list[3])
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
        elif flag == 1:  # ok
            self.cfgPar.add_serial_config(dic)
            pass
        else:
            pass
        self.newConnect.NewConSignal.disconnect()

    def slot_Serial_emit(self, flag, data):
        if flag == 0:  # rec
            # hex显示
            if self.cfgPar.get_show_format() == 'hex':
                out_s = ''
                for i in range(0, len(data)):
                    out_s = out_s + '{:02X}'.format(data[i]) + ' '
                self.textEditRecvive.insertPlainText(out_s)
            else:# 串口接收到的字符串为b'123',要转化成unicode字符串才能输出到窗口中去
                out_s = data.decode('utf-8')
                data_s = acHandler.show_parse(out_s)
            #    print(out_s+"stop")
                self.textEditRecvive.insertPlainText(out_s)
            textCursor = self.textEditRecvive.textCursor()
            textCursor.movePosition(textCursor.End)
            self.textEditRecvive.setTextCursor(textCursor)
        elif flag == 1:  # send
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

    def slot_filter_by_level(self):
        pass

    def slot_filter_by_tag(self):
        pass

    def slot_ipc_parser(self):
        pass

