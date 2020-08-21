from PyQt5 import QtGui
from PyQt5.QtGui import QTextCursor

import mainwindow as UI_main
import newconnecthandler as NC_handler
import openconnecthandler as OC_handler
from PyQt5.QtWidgets import QApplication, QMainWindow
import serialprocess as mySerial
from PyQt5.QtWidgets import QMessageBox
import configutil as Config
from main import global_data as g_data
import binascii
import ipchandler as Ipc
import chartranshandler
import filetranshandler


class MyMainWindow(QMainWindow, UI_main.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.ser = mySerial.serialProcess()  # 实例串口类

        self.cfgPar = Config.configParser()  # 实例配置项类,界面同步部分配置项
        self.configInit()

        self.ipcParse = Ipc.ipcHandler()
        self.lineEditinputIPC_doc.setText(self.cfgPar.get_ipc_document())

        # 子窗口需要为主窗口的成员变量，否则子窗口会一闪而过
        self.newConnect = NC_handler.MyNewConnect()  # 新连接的窗口
        self.openConnect = OC_handler.MyOpenConnect()  # 打开的窗口

        self.buildConnect()

        self.slot_change_transfer()
        self.slot_OpenConnect()
        # TODO
        self.lineEditinputIPC_file.setEnabled(False)

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
                    self.cfgPar.set_config('sendRecord', 'send'+str(i), text)
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
        g_data.rec_show['time'] = True if self.actionTime.isChecked() else False

        self.actionASCII.setChecked((self.cfgPar.get_show_format() is 'asc'))
        self.actionHEX.setChecked((self.actionASCII.isChecked() is False))
        g_data.rec_show['format'] = self.cfgPar.get_show_format()

        self.actionSendASCII.setChecked((self.cfgPar.get_send_format() is 'asc'))
        self.actionSendHEX.setChecked((self.actionSendASCII.isChecked() is False))
        g_data.send_show['format'] = self.cfgPar.get_send_format()

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

    def buildConnect(self):
        self.buttonSend.clicked.connect(self.slot_SendMessage)
        self.lineEdit.returnPressed.connect(self.slot_SendMessage2)

        self.actionNew.triggered.connect(self.slot_NewConnect)
        self.actionOpen.triggered.connect(self.slot_OpenConnect)

        self.actionDisconnect.triggered.connect(self.ser.port_close)
        self.actionRe_Connect.triggered.connect(self.ser.port_connect)

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
        self.button_transchar.clicked.connect(self.slot_hex_to_ascii)  # 十六进制转换ascii码
        self.button_transHEX.clicked.connect(self.slot_ascii_to_hex)  # ascii码转换十六进制

        self.buttonstartTrans.clicked.connect(self.slot_start_transfer)  # 文件格式转换
        self.comboBoxfiletrans.currentIndexChanged.connect(self.slot_change_transfer)  # 文件格式转换功能选择

    def slot_SendMessage(self):
        text = self.lineEditSend.currentText().strip()
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
                            return None
                        text = text[2:].strip()
                        send_list.append(num)
                    input_s = bytes(send_list)
                else:
                    if text.endswith('\n'):
                        input_s = text.encode('utf-8')
                    else:
                        input_s = (text + '\n').encode('utf-8')
                self.ser.port_send(input_s)
            self.textEditRecvive.append(text)
            self.textEditRecvive.moveCursor(QTextCursor.End)
            if self.lineEditSend.itemText(0) == text:
                pass
            else:
                self.lineEditSend.insertItem(0, text)

    def slot_SendMessage2(self):
        text = self.lineEdit.text().strip()
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
                            return None
                        text = text[2:].strip()
                        send_list.append(num)
                    input_s = bytes(send_list)
                else:
                    if text.endswith('\n'):
                        input_s = text.encode('utf-8')
                    else:
                        input_s = (text + '\n').encode('utf-8')
                self.ser.port_send(input_s)
        else:
            self.ser.port_send('\n'.encode('utf-8'))
            self.textEditRecvive.append(text)
            self.textEditRecvive.moveCursor(QTextCursor.End)

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

    def slot_show_time(self):
        value = True if self.actionTime.isChecked() else False
        g_data.rec_show['time'] = value
        self.cfgPar.set_config('showCfg', 'show_time', str(value))

    def slot_show_asc(self):
        if self.actionASCII.isChecked():
            value = 'asc'
            self.actionHEX.setChecked(False)
        else:
            value = 'hex'
            self.actionHEX.setChecked(True)
        g_data.rec_show['format'] = value
        self.cfgPar.set_config('showCfg', 'show_format', value)

    def slot_send_asc(self):
        if self.actionSendASCII.isChecked():
            value = 'asc'
            self.actionSendHEX.setChecked(False)
        else:
            value = 'hex'
            self.actionSendHEX.setChecked(True)
        g_data.send_show['format'] = value
        self.cfgPar.set_config('sendCfg', 'send_format', value)

    def slot_show_hex(self):
        if self.actionHEX.isChecked():
            value = 'hex'
            self.actionASCII.setChecked(False)
        else:
            value = 'asc'
            self.actionASCII.setChecked(True)
        g_data.rec_show['format'] = value
        self.cfgPar.set_config('showCfg', 'show_format', value)

    def slot_send_hex(self):
        if self.actionSendHEX.isChecked():
            value = 'hex'
            self.actionSendASCII.setChecked(False)
        else:
            value = 'asc'
            self.actionSendASCII.setChecked(True)
        g_data.send_show['format'] = value
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
        inputStr = self.lineEditinputIPC.text()
        inputXml = self.lineEditinputIPC_doc.text()
        self.textEditoutputIPC.clear()
        if inputXml.endswith('.xml') and inputXml != self.cfgPar.get_ipc_document():
            self.cfgPar.set_config('ipcCfg', 'document', inputXml)
        if inputStr is not '':
            outStr = self.ipcParse.parseIpcData(inputStr, inputXml)
        self.textEditoutputIPC.insertPlainText(outStr)

    def slot_hex_to_ascii(self):
        inputStr = self.textEdit_beforetrans.toPlainText()
        self.textEdit_aftertrans.clear()
        if inputStr is not '':
            outStr = chartranshandler.hex2ascii(inputStr)
        self.textEdit_aftertrans.insertPlainText(outStr)

    def slot_ascii_to_hex(self):
        inputStr = self.textEdit_beforetrans.toPlainText()
        self.textEdit_aftertrans.clear()
        if inputStr is not '':
            outStr = chartranshandler.ascii2hex(inputStr)
        self.textEdit_aftertrans.insertPlainText(outStr)

    def slot_start_transfer(self):
        index = self.comboBoxfiletrans.currentIndex()
        if index is 0:
            filetranshandler.hexToBin(self.lineEdit_sourse.text(), self.lineEdit_start1.text(), self.lineEdit_end1.text(),
                                      self.lineEdit_obj.text(), self.lineEdit_start3.text(), self.lineEdit_end3.text(),
                                      self.lineEdit_pad.text())
        elif index is 1:
            filetranshandler.binToHex(self.lineEdit_sourse.text(), self.lineEdit_obj.text(), self.lineEdit_start1.text())
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
