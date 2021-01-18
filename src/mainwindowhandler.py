import time
import datetime
from random import random

from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QTextCursor

import mainwindow as UI_main
import newconnecthandler as NC_handler
import openconnecthandler as OC_handler
from PyQt5.QtWidgets import QMainWindow, QGridLayout
import serialprocess as mySerial
from PyQt5.QtWidgets import QMessageBox
import configutil as Config
import ipchandler as Ipc
import chartranshandler
import filetranshandler
import plotterhandler as Plotter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtCore import pyqtSlot
import numpy as np


class MyMainWindow(QMainWindow, UI_main.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionRe_Connect)
        self.toolBar.addAction(self.actionDisconnect)
        self.toolBar.addAction(self.menuShow.menuAction())

        self.ser = mySerial.serialProcess()  # 实例串口类

        # 定时器发送数据auto
        self.timer_send = QTimer()
        self.timer_send.timeout.connect(self.send_message_auto)

        # 定时器发送数据porting
        self.timer_polling = QTimer()
        self.timer_polling.timeout.connect(self.send_polling_message)

        self.auto_send_cnt = 0
        self.auto_send_message = ''
        self.polling_send_cnt = 0
        self.polling_current_send = 0
        self.polling_send_message_list = []
        self.polling_lineEdit = [self.lineEdit_send2, self.lineEditsend3, self.lineEditsend4, self.lineEditsend5,
                                 self.lineEditsend6, self.lineEditsend7, self.lineEditsend8, self.lineEditsend9,
                                 self.lineEditsend10, self.lineEditsend11]
        self.polling_checkbox = [self.checkBoxpolling1, self.checkBoxpolling2, self.checkBoxpolling3,
                                 self.checkBoxpolling4, self.checkBoxpolling5, self.checkBoxpolling6,
                                 self.checkBoxpolling7, self.checkBoxpolling8,
                                 self.checkBoxpolling9, self.checkBoxpolling10]

        self.cfgPar = Config.configParser()  # 实例配置项类,界面同步部分配置项
        self.configInit()

        self.ipcParse = Ipc.ipcHandler()
        self.lineEditinputIPC_doc.setText(self.cfgPar.get_ipc_document())
        self.lineEditinputIPC_doc_2.setText(self.cfgPar.get_ipc_logdescription())
        self.lineEditinputIPC_file_obj.setText(self.cfgPar.get_ipc_logoutput())
        # 子窗口需要为主窗口的成员变量，否则子窗口会一闪而过
        self.newConnect = NC_handler.MyNewConnect()  # 新连接的窗口
        self.openConnect = OC_handler.MyOpenConnect()  # 打开的窗口

        # plotter init start
        self.fig = Plotter.dynamic_fig(width=5, height=3, dpi=72)
        # add NavigationToolbar in the figure (widgets)
        self.fig_ntb = NavigationToolbar(self.fig, self)
        # add the dynamic_fig in the Plot box
        self.gridlayout = QGridLayout(self.groupBox_plot)
        self.gridlayout.addWidget(self.fig)
        self.gridlayout.addWidget(self.fig_ntb)
        # initialized flags for static/dynamic plot: on is 1,off is 0
        self._timer = QTimer(self)
        self._t = 0.0
        self.y1 = [0, ]
        self.y2 = [0, ]
        self.y3 = [0, ]
        self.y4 = [0, ]
        self._cur = [0, 0, 0, 0]
        self._i = 0
        self.start_flag = 0
        self._delay_t = [0.0, ]
        self._update_on = 0
        # plotter init end

        self.buildConnect()
        self.slot_change_transfer()
        self.actionDisconnect.setEnabled(False)
        self.actionRe_Connect.setEnabled(False)
        self.slot_OpenConnect()
        # TODO
        self.lineEdit_source2.setEnabled(False)
        self.lineEdit_start2.setEnabled(False)
        self.lineEdit_end2.setEnabled(False)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        reply = QMessageBox.question(self, 'Serial Tool', "是否要退出程序？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.lineEditSend.count() > 0:
                count = self.lineEditSend.count()
                i = 0
                while i < count:
                    text = self.lineEditSend.itemText(i)
                    self.cfgPar.set_config('sendRecord', 'send' + str(i), text)
                    i = i + 1
            self.cfgPar.write_to_config()
            self.ser.port_close()
            self.newConnect.destroy()
            self.openConnect.destroy()
            self.destroy()
            a0.accept()
        else:
            a0.ignore()

    def configInit(self):
        self.actionTime.setChecked(self.cfgPar.is_show_time())

        if self.cfgPar.get_show_format() == 'asc':
            self.actionASCII.setChecked(True)
            self.actionHEX.setChecked(False)
        else:
            self.actionASCII.setChecked(False)
            self.actionHEX.setChecked(True)

        if self.cfgPar.get_send_format() == 'asc':
            self.actionSendASCII.setChecked(True)
            self.actionSendHEX.setChecked(False)
        else:
            self.actionSendASCII.setChecked(False)
            self.actionSendHEX.setChecked(True)

        self.tabWidget.setVisible(self.cfgPar.get_right_hide() is '0')
        self.actionhideright.setChecked(self.cfgPar.get_right_hide() is '1')
        if self.cfgPar.get_send_line_hide() is '1':
            self.actionhideSend.setChecked(True)
            self.buttonSend.setVisible(False)
            self.lineEditSend.setVisible(False)
            self.lineEdit.setVisible(False)
        else:
            self.actionhideSend.setChecked(False)
            if self.cfgPar.get_send_button_hide() is '1':
                self.actionHidesendbutton.setChecked(True)
                self.buttonSend.setVisible(False)
                self.lineEditSend.setVisible(False)
                self.lineEdit.setVisible(True)
            else:
                self.actionHidesendbutton.setChecked(False)
                self.buttonSend.setVisible(True)
                self.lineEditSend.setVisible(True)
                self.lineEdit.setVisible(False)

        for item in self.cfgPar.get_send_record():
            if item is not '':
                self.lineEditSend.addItem(item)

        self.lineEditsend1.setText(self.cfgPar.get_auto_send_record())
        self.spinBoxcnt1.setValue(self.cfgPar.get_auto_send_cnt())
        self.spinBoxtime1.setValue(self.cfgPar.get_auto_send_time())
        polling_index = 0
        for send_text in self.cfgPar.get_porting_send_record():
            self.polling_lineEdit[polling_index].setText(send_text)
            polling_index += 1

    def buildConnect(self):
        self.buttonSend.clicked.connect(self.slot_SendMessage)
        self.lineEdit.returnPressed.connect(self.slot_SendMessage2)
        self.buttonSend_2.clicked.connect(self.slot_SendMessage_auto)
        self.buttonSend_3.clicked.connect(self.slot_send_polling_message)

        self.buttonSend_CtrlC.clicked.connect(self.slot_send_CtrlC)

        self.actionNew.triggered.connect(self.slot_NewConnect)
        self.actionOpen.triggered.connect(self.slot_OpenConnect)

        self.actionDisconnect.triggered.connect(self.slot_close_port)
        self.actionRe_Connect.triggered.connect(self.slot_reconnect)
        self.actionClear_All.triggered.connect(self.slot_clear_all)

        self.actionTime.triggered.connect(self.slot_show_time)  # 显示时间
        self.actionASCII.triggered.connect(self.slot_show_asc)
        self.actionHEX.triggered.connect(self.slot_show_hex)
        self.actionSendASCII.triggered.connect(self.slot_send_asc)
        self.actionSendHEX.triggered.connect(self.slot_send_hex)

        self.actionhideright.triggered.connect(self.slot_hide_right)
        self.actionhideSend.triggered.connect(self.slot_hide_send)
        self.actionHidesendbutton.triggered.connect(self.slot_hide_send_button)

        self.ser.SerialSignal.connect(self.slot_Serial_emit)

        self.button_ipcparse.clicked.connect(self.slot_ipc_data_parse)  # ipc单条数据解析
        self.button_ipcparse_2.clicked.connect(self.slot_ipc_file_parse)
        self.button_ipcparse_tip.clicked.connect(self.slot_ipc_tip_generate)
        self.button_transchar.clicked.connect(self.slot_hex_to_ascii)  # 十六进制转换ascii码
        self.button_transHEX.clicked.connect(self.slot_ascii_to_hex)  # ascii码转换十六进制
        self.button_transspace.clicked.connect(self.slot_hex_add_space)  # ascii码转换十六进制

        self.buttonstartTrans.clicked.connect(self.slot_start_transfer)  # 文件格式转换
        self.comboBoxfiletrans.currentIndexChanged.connect(self.slot_change_transfer)  # 文件格式转换功能选择

    def slot_close_port(self):
        self.ser.port_close()
        if self.ser.serial.isOpen():
            self.textEditRecvive.insertPlainText(self.ser.serial.port + " can not be closed\r\n")
        else:
            self.textEditRecvive.insertPlainText(self.ser.serial.port + " is closed\r\n")

    def slot_reconnect(self):
        self.ser.port_close()
        self.ser.port_connect()
        if self.ser.serial.isOpen():
            self.textEditRecvive.insertPlainText(self.ser.serial.port + " is connected\r\n")
        else:
            self.textEditRecvive.insertPlainText(self.ser.serial.port + " can not be connected\r\n")

    def slot_clear_all(self):
        self.textEditRecvive.clear()

    def parse_sendMessage(self, text):
        text_list = text.split(' ')
        if "" != text:
            if text_list[0] == 'config':
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
                            return ''
                        text = text[2:].strip()
                        send_list.append(num)
                    input_s = bytes(send_list)
                else:
                    if text.endswith('\n'):
                        input_s = text.encode('utf-8')
                    else:
                        input_s = (text + '\n').encode('utf-8')
                return input_s
        return ''

    def slot_send_CtrlC(self):
        send_list = [int('3', 16)]
        input_s = bytes(send_list)
        print("send ctrl c")
        self.ser.port_send(input_s)

    def slot_SendMessage(self):
        text = self.lineEditSend.currentText().strip()
        input_s = self.parse_sendMessage(text)
        if input_s != '':
            self.ser.port_send(input_s)
            if self.lineEditSend.itemText(0) == text:
                pass
            else:
                self.lineEditSend.insertItem(0, text)
        self.textEditRecvive.moveCursor(QTextCursor.End)

    def slot_SendMessage2(self):
        text = self.lineEdit.text().strip()
        input_s = self.parse_sendMessage(text)
        if input_s != '':
            print("send")
            self.ser.port_send(input_s)
        else:
            self.ser.port_send('\n'.encode('utf-8'))
        self.textEditRecvive.moveCursor(QTextCursor.End)
        self.lineEdit.selectAll()

    def slot_SendMessage_auto(self):
        if self.buttonSend_2.text() == '开始发送':
            self.buttonSend_2.setText('停止发送')
            text = self.lineEditsend1.text().strip()
            self.auto_send_message = self.parse_sendMessage(text)
            self.auto_send_cnt = self.spinBoxcnt1.value()
            time = self.spinBoxtime1.value()
            if self.auto_send_message != '':
                self.cfgPar.set_auto_send(text, str(self.auto_send_cnt), str(time))
            self.lineEditsend1.setEnabled(False)
            self.spinBoxtime1.setEnabled(False)
            self.spinBoxcnt1.setEnabled(False)
            self.timer_send.start(time)
        elif self.buttonSend_2.text() == '停止发送':
            if self.timer_send.isActive():
                self.timer_send.stop()
            self.lineEditsend1.setEnabled(True)
            self.spinBoxtime1.setEnabled(True)
            self.spinBoxcnt1.setEnabled(True)
            self.buttonSend_2.setText('开始发送')

    def send_message_auto(self):
        if self.auto_send_cnt > 0:
            if self.auto_send_message != '':
                self.ser.port_send(self.auto_send_message)
                self.textEditRecvive.moveCursor(QTextCursor.End)
                self.auto_send_cnt = self.auto_send_cnt - 1
        elif self.auto_send_cnt == 0:
            self.slot_SendMessage_auto()
        elif self.auto_send_cnt == -1:
            if self.auto_send_message != '':
                self.ser.port_send(self.auto_send_message)
                self.textEditRecvive.moveCursor(QTextCursor.End)

    def slot_send_polling_message(self):
        if self.buttonSend_3.text() == '开始发送':
            self.buttonSend_3.setText('停止发送')
            self.polling_send_message_list.clear()
            for i in range(0, 10):
                text = self.polling_lineEdit[i].text().strip()
                if text != '' and self.polling_checkbox[i].isChecked():
                    sendMessage = self.parse_sendMessage(text)
                    if sendMessage != '':
                        self.polling_send_message_list.append(sendMessage)
                        print(i, text)
                        self.cfgPar.set_polling_send_message(str(i + 1), text)
                self.polling_lineEdit[i].setEnabled(False)
                self.polling_checkbox[i].setEnabled(False)
            print(self.polling_send_message_list)
            self.polling_send_cnt = self.spinBoxcnt2.value()
            time = self.doubleSpinBoxtime.value() * 1000
            self.cfgPar.set_polling_send_cnt_time(str(self.polling_send_cnt), str(time))
            self.polling_current_send = 0
            self.timer_polling.start(time)
            print(time, self.polling_send_cnt)
        elif self.buttonSend_3.text() == '停止发送':
            if self.timer_polling.isActive():
                self.timer_polling.stop()
            for i in range(0, 10):
                self.polling_lineEdit[i].setEnabled(True)
                self.polling_checkbox[i].setEnabled(True)
            self.buttonSend_3.setText('开始发送')

    def send_polling_message(self):
        if self.polling_send_cnt > 0:
            message_list_len = len(self.polling_send_message_list)
            if message_list_len > 0:
                text = self.polling_send_message_list[self.polling_current_send]
                self.ser.port_send(text)
                self.textEditRecvive.moveCursor(QTextCursor.End)
                self.polling_current_send = self.polling_current_send + 1
                if self.polling_current_send == message_list_len:
                    self.polling_current_send = 0
                    self.polling_send_cnt = self.polling_send_cnt - 1
                print(self.polling_current_send)
            else:
                print("send_polling_message list len is 0")
        elif self.polling_send_cnt == 0:
            self.slot_send_polling_message()
        elif self.polling_send_cnt == -1:
            text = self.polling_send_message_list.index(self.polling_current_send)
            self.ser.port_send(text)
            self.textEditRecvive.moveCursor(QTextCursor.End)
            self.polling_current_send = self.polling_current_send + 1
            if self.polling_current_send == self.polling_send_message_list.count():
                self.polling_current_send = 0

    def slot_NewConnect(self):
        self.newConnect.set_PortList(self.ser.Com_List)
        self.newConnect.update_port_id(self.cfgPar.get_serial_config_list())
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
                self.actionDisconnect.setEnabled(True)
            else:
                self.textEditRecvive.insertPlainText(dic['port'] + " can not be connected\r\n")
        elif flag == 1:
            self.newConnect.close()
            self.slot_NewConnect()
        elif flag == 2:  # delete
            self.cfgPar.delete_serial_config(dic)

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
            self.plot_data_parse(data)
            out_str = data.decode('utf-8', 'ignore')
            if self.cfgPar.get_show_format() == 'hex':
                out_s = chartranshandler.ascii2hex(out_str)
                self.textEditRecvive.insertPlainText(out_s)
            else:
                self.textEditRecvive.insertPlainText(out_str)
            textCursor = self.textEditRecvive.textCursor()
            textCursor.movePosition(textCursor.End)
            self.textEditRecvive.setTextCursor(textCursor)
        elif flag == 'error':
            self.ser.port_close()

    def slot_show_time(self):
        value = True if self.actionTime.isChecked() else False
        self.cfgPar.set_config('showCfg', 'show_time', str(value))

    def slot_show_asc(self):
        if self.actionASCII.isChecked():
            value = 'asc'
            self.actionHEX.setChecked(False)
        else:
            value = 'hex'
            self.actionHEX.setChecked(True)
        self.cfgPar.set_config('showCfg', 'show_format', value)

    def slot_send_asc(self):
        if self.actionSendASCII.isChecked():
            value = 'asc'
            self.actionSendHEX.setChecked(False)
        else:
            value = 'hex'
            self.actionSendHEX.setChecked(True)
        self.cfgPar.set_config('sendCfg', 'send_format', value)

    def slot_show_hex(self):
        if self.actionHEX.isChecked():
            value = 'hex'
            self.actionASCII.setChecked(False)
        else:
            value = 'asc'
            self.actionASCII.setChecked(True)
        self.cfgPar.set_config('showCfg', 'show_format', value)

    def slot_send_hex(self):
        if self.actionSendHEX.isChecked():
            value = 'hex'
            self.actionSendASCII.setChecked(False)
        else:
            value = 'asc'
            self.actionSendASCII.setChecked(True)
        self.cfgPar.set_config('sendCfg', 'send_format', value)

    def slot_hide_right(self):
        if self.actionhideright.isChecked():
            self.tabWidget.setVisible(False)
            self.cfgPar.set_config('windowHide', 'right', '1')
        else:
            self.tabWidget.setVisible(True)
            self.cfgPar.set_config('windowHide', 'right', '0')

    def slot_hide_send(self):
        if self.actionhideSend.isChecked():
            self.lineEditSend.setVisible(False)
            self.buttonSend.setVisible(False)
            self.lineEdit.setVisible(False)
            self.cfgPar.set_config('windowHide', 'send_line', '1')
            self.actionHidesendbutton.setChecked(False)
        else:
            self.cfgPar.set_config('windowHide', 'send_line', '0')
            if self.actionHidesendbutton.isChecked():
                self.lineEdit.setVisible(True)
                self.buttonSend.setVisible(False)
                self.lineEditSend.setVisible(False)
            else:
                self.lineEditSend.setVisible(True)
                self.buttonSend.setVisible(True)
                self.lineEdit.setVisible(False)

    def slot_hide_send_button(self):
        if self.actionHidesendbutton.isChecked():
            self.cfgPar.set_config('windowHide', 'send_button', '1')
            self.lineEditSend.setVisible(False)
            self.buttonSend.setVisible(False)
            self.lineEdit.setVisible(True)
            self.actionhideSend.setChecked(False)
        else:
            self.cfgPar.set_config('windowHide', 'send_button', '0')
            self.lineEditSend.setVisible(True)
            self.buttonSend.setVisible(True)
            self.lineEdit.setVisible(False)

    def slot_ipc_data_parse(self):
        outStr = ''
        inputStr = self.lineEditinputIPC.text()
        inputXml = self.lineEditinputIPC_doc.text()
        inputLog = self.lineEditinputIPC_doc_2.text()
        self.textEditoutputIPC.clear()
        if inputXml.endswith('.xml') and inputXml != self.cfgPar.get_ipc_document():
            self.cfgPar.set_config('ipcCfg', 'document', inputXml)
        if inputLog != self.cfgPar.get_ipc_logdescription():
            self.cfgPar.set_config('ipcCfg', 'logdescription', inputLog)
        inputlog_list = inputLog.split('|')
        if inputStr != '':
            outStr = self.ipcParse.parseIpcData(inputStr, inputXml, inputlog_list)
        self.textEditoutputIPC.insertPlainText(outStr)

    def slot_ipc_tip_generate(self):
        self.ipcParse.generate_tips_file(self.lineEditinputIPC_doc.text())

    def slot_ipc_file_parse(self):
        outfile = self.lineEditinputIPC_file_obj.text()
        inputfile = self.lineEditinputIPC_file_src.text()
        inputXml = self.lineEditinputIPC_doc.text()
        inputLog = self.lineEditinputIPC_doc_2.text()
        self.textEditoutputIPC.clear()
        if inputXml.endswith('.xml') and inputXml != self.cfgPar.get_ipc_document():
            self.cfgPar.set_config('ipcCfg', 'document', inputXml)
        if outfile != self.cfgPar.get_ipc_logoutput():
            self.cfgPar.set_config('ipcCfg', 'outputfile', outfile)
        if inputLog != self.cfgPar.get_ipc_logdescription():
            self.cfgPar.set_config('ipcCfg', 'logdescription', inputLog)
        inputlog_list = inputLog.split('|')
        if inputfile.endswith('.txt'):
            self.ipcParse.parseIpcFile_soc(inputfile, outfile, inputXml, inputlog_list)

    def slot_hex_to_ascii(self):
        outStr = ''
        inputStr = self.textEdit_beforetrans.toPlainText()
        self.textEdit_aftertrans.clear()
        if inputStr is not '':
            outStr = chartranshandler.hex2ascii(inputStr)
        self.textEdit_aftertrans.insertPlainText(outStr)

    def slot_ascii_to_hex(self):
        outStr = ''
        inputStr = self.textEdit_beforetrans.toPlainText()
        self.textEdit_aftertrans.clear()
        if inputStr is not '':
            outStr = chartranshandler.ascii2hex(inputStr)
        self.textEdit_aftertrans.insertPlainText(outStr)

    def slot_hex_add_space(self):
        outStr = ''
        inputStr = self.textEdit_beforetrans.toPlainText()
        self.textEdit_aftertrans.clear()
        if inputStr is not '':
            outStr = chartranshandler.hexaddspace(inputStr)
        self.textEdit_aftertrans.insertPlainText(outStr)

    def slot_start_transfer(self):
        index = self.comboBoxfiletrans.currentIndex()
        if index is 0:
            filetranshandler.hexToBin(self.lineEdit_sourse.text(), self.lineEdit_start1.text(),
                                      self.lineEdit_end1.text(),
                                      self.lineEdit_obj.text(), self.lineEdit_start3.text(), self.lineEdit_end3.text(),
                                      self.lineEdit_pad.text())
        elif index is 1:
            filetranshandler.binToHex(self.lineEdit_sourse.text(), self.lineEdit_obj.text(),
                                      self.lineEdit_start1.text())
        elif index is 2:
            filetranshandler.binToTxt(self.lineEdit_sourse.text(), self.lineEdit_obj.text())
        elif index is 3:
            filetranshandler.txtToBin(self.lineEdit_sourse.text(), self.lineEdit_obj.text())

    def slot_change_transfer(self):
        index = self.comboBoxfiletrans.currentIndex()
        if index is 0:
            self.lineEdit_start1.setEnabled(True)
            self.lineEdit_end1.setEnabled(True)
            self.lineEdit_start3.setEnabled(True)
            self.lineEdit_end3.setEnabled(True)
            self.lineEdit_pad.setEnabled(True)
        elif index is 1:
            self.lineEdit_start1.setEnabled(True)
            self.lineEdit_end1.setEnabled(False)
            self.lineEdit_start3.setEnabled(False)
            self.lineEdit_end3.setEnabled(False)
            self.lineEdit_pad.setEnabled(False)
        elif index is 2:
            self.lineEdit_start1.setEnabled(False)
            self.lineEdit_end1.setEnabled(False)
            self.lineEdit_start3.setEnabled(False)
            self.lineEdit_end3.setEnabled(False)
            self.lineEdit_pad.setEnabled(False)
        elif index is 3:
            self.lineEdit_start1.setEnabled(False)
            self.lineEdit_end1.setEnabled(False)
            self.lineEdit_start3.setEnabled(False)
            self.lineEdit_end3.setEnabled(False)
            self.lineEdit_pad.setEnabled(False)

    @pyqtSlot()
    def on_pushButton_plot_clicked(self):
        if self._update_on == 0:
            self._update_on = 1
            self._timer.timeout.connect(self.update_fig)
            self._timer.start(100)  # plot after 100ms delay
            self._t = time.time()
            self.groupBox_10.setEnabled(False)
            self.groupBox_9.setEnabled(False)
            self.pushButton_plot.setText("停止")
        elif self._update_on == 1:
            self._update_on = 0
            self._timer.timeout.disconnect(self.update_fig)
            self._timer.stop()
            self.groupBox_10.setEnabled(True)
            self.groupBox_9.setEnabled(True)
            self.pushButton_plot.setText("开始")

    def update_fig(self):
        self.fig.axes.cla()
        if self.checkbox_graph1.isChecked():
            self.fig.axes.plot(self._delay_t, self.y1, color="red", marker='o')
        if self.checkBox_graph2.isChecked():
            self.fig.axes.plot(self._delay_t, self.y2, color="orange", marker='o')
        if self.checkBox_graph3.isChecked():
            self.fig.axes.plot(self._delay_t, self.y3, color="blue", marker='o')
        if self.checkBox_graph4.isChecked():
            self.fig.axes.plot(self._delay_t, self.y4, color="green", marker='o')
        self.fig.axes.set_title("signals")
        self.fig.axes.set_xlabel("time(s)")
        self.fig.axes.set_ylabel("data")
        self.fig.axes.grid(color='black', linestyle='--', linewidth=1, alpha=0.3)
        self.fig.draw()

    @pyqtSlot()
    def on_pushButton_pic_2_clicked(self):
        self._delay_t = []
        self.y1 = []
        self.y2 = []
        self.y3 = []
        self.y4 = []
        self.fig.axes.cla()
        counts = [0, 1]
        delay_t = [0, 1]
        self.fig.axes.plot(delay_t, counts)
        self.fig.axes.set_title("signals")
        self.fig.axes.set_xlabel("time(s)")
        self.fig.axes.set_ylabel("data")
        self.fig.axes.grid(color='black', linestyle='--', linewidth=1, alpha=0.3)
        self.fig.draw()

    def plot_data_parse(self, data):
        if self._update_on:
            for ch in data:
                if ch == 0x7E and self.start_flag == 0:
                    self.start_flag = 1
                    continue
                if ch == 0x55 and self.start_flag == 1:
                    if self._i == 4:
                        self.start_flag = 0
                        self._i = 0
                        if self.radioButton.isChecked():
                            self.y1.append(self._cur[0])
                            self.y2.append(self._cur[1])
                            self.y3.append(self._cur[2])
                            self.y4.append(self._cur[3])
                        elif self.radioButton_2.isChecked():
                            self.y1.append(self._cur[0] << 8 + self._cur[1])
                            self.y2.append(self._cur[2] << 8 + self._cur[3])
                        elif self.radioButton_3.isChecked():
                            self.y1.append(self._cur[0] << 24 + self._cur[1] << 16 + self._cur[2] << 8 + self._cur[3])
                        t = time.time()
                        t = t - self._t
                        self._delay_t.append(t)
                if self.start_flag and self._i < 4:
                    self._cur[self._i] = ch
                    self._i = self._i + 1

    @pyqtSlot()
    def on_radioButton_clicked(self):
        self.checkbox_graph1.setChecked(True)
        self.checkBox_graph2.setChecked(True)
        self.checkBox_graph3.setChecked(True)
        self.checkBox_graph4.setChecked(True)

    @pyqtSlot()
    def on_radioButton_2_clicked(self):
        self.checkbox_graph1.setChecked(True)
        self.checkBox_graph2.setChecked(True)
        self.checkBox_graph3.setChecked(False)
        self.checkBox_graph4.setChecked(False)

    @pyqtSlot()
    def on_radioButton_3_clicked(self):
        self.checkbox_graph1.setChecked(True)
        self.checkBox_graph2.setChecked(False)
        self.checkBox_graph3.setChecked(False)
        self.checkBox_graph4.setChecked(False)
