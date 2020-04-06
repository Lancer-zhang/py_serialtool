# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.textEditRecvive = QtWidgets.QTextBrowser(self.centralwidget)
        self.textEditRecvive.setStyleSheet("background-color: balck; color: white;")
        self.textEditRecvive.setObjectName("textEditRecvive")
        self.gridLayout.addWidget(self.textEditRecvive, 0, 0, 1, 2)
        self.lineEditSend = QtWidgets.QComboBox(self.centralwidget)
        self.lineEditSend.setEditable(True)
        self.lineEditSend.setObjectName("lineEditSend")
        self.gridLayout.addWidget(self.lineEditSend, 1, 0, 1, 1)
        self.buttonSend = QtWidgets.QPushButton(self.centralwidget)
        self.buttonSend.setMaximumSize(QtCore.QSize(100, 16777215))
        self.buttonSend.setObjectName("buttonSend")
        self.gridLayout.addWidget(self.buttonSend, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1038, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuLog = QtWidgets.QMenu(self.menuFile)
        self.menuLog.setObjectName("menuLog")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuFilter = QtWidgets.QMenu(self.menuView)
        self.menuFilter.setObjectName("menuFilter")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuOption = QtWidgets.QMenu(self.menubar)
        self.menuOption.setObjectName("menuOption")
        self.menuShow = QtWidgets.QMenu(self.menuOption)
        self.menuShow.setObjectName("menuShow")
        self.menuWindow = QtWidgets.QMenu(self.menubar)
        self.menuWindow.setObjectName("menuWindow")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.hide()
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        MainWindow.insertToolBarBreak(self.toolBar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionDisconnect = QtWidgets.QAction(MainWindow)
        self.actionDisconnect.setObjectName("actionDisconnect")
        self.actionRe_Connect = QtWidgets.QAction(MainWindow)
        self.actionRe_Connect.setEnabled(False)
        self.actionRe_Connect.setObjectName("actionRe_Connect")
        self.actionImport = QtWidgets.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")
        self.actionExport = QtWidgets.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionOtherSave = QtWidgets.QAction(MainWindow)
        self.actionOtherSave.setObjectName("actionOtherSave")
        self.actionStart = QtWidgets.QAction(MainWindow)
        self.actionStart.setObjectName("actionStart")
        self.actionStop = QtWidgets.QAction(MainWindow)
        self.actionStop.setObjectName("actionStop")
        self.actionPause = QtWidgets.QAction(MainWindow)
        self.actionPause.setObjectName("actionPause")
        self.actionContinue = QtWidgets.QAction(MainWindow)
        self.actionContinue.setObjectName("actionContinue")
        self.actionOpenFile = QtWidgets.QAction(MainWindow)
        self.actionOpenFile.setObjectName("actionOpenFile")
        self.actionOpenLog = QtWidgets.QAction(MainWindow)
        self.actionOpenLog.setObjectName("actionOpenLog")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionCut = QtWidgets.QAction(MainWindow)
        self.actionCut.setObjectName("actionCut")
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.actionClearCache = QtWidgets.QAction(MainWindow)
        self.actionClearCache.setObjectName("actionClearCache")
        self.actionClear_All = QtWidgets.QAction(MainWindow)
        self.actionClear_All.setObjectName("actionClear_All")
        self.actionFind = QtWidgets.QAction(MainWindow)
        self.actionFind.setObjectName("actionFind")
        self.actionFind_All = QtWidgets.QAction(MainWindow)
        self.actionFind_All.setObjectName("actionFind_All")
        self.actionOptions = QtWidgets.QAction(MainWindow)
        self.actionOptions.setObjectName("actionOptions")
        self.actionFast_cmd = QtWidgets.QAction(MainWindow)
        self.actionFast_cmd.setObjectName("actionFast_cmd")
        self.actionClolor = QtWidgets.QAction(MainWindow)
        self.actionClolor.setObjectName("actionClolor")
        self.actionIPC_parse = QtWidgets.QAction(MainWindow)
        self.actionIPC_parse.setObjectName("actionIPC_parse")
        self.actionIPC_parse.setCheckable(True)
        self.actionBy_level = QtWidgets.QAction(MainWindow)
        self.actionBy_level.setObjectName("actionBy_level")
        self.actionBy = QtWidgets.QAction(MainWindow)
        self.actionBy.setObjectName("actionBy")
        self.actionBy_function = QtWidgets.QAction(MainWindow)
        self.actionBy_function.setObjectName("actionBy_function")
        self.actionBy_file = QtWidgets.QAction(MainWindow)
        self.actionBy_file.setObjectName("actionBy_file")
        self.actionDefine = QtWidgets.QAction(MainWindow)
        self.actionDefine.setObjectName("actionDefine")
        self.actionTime = QtWidgets.QAction(MainWindow)
        self.actionTime.setCheckable(True)
        self.actionTime.setObjectName("actionTime")
        self.actionTag = QtWidgets.QAction(MainWindow)
        self.actionTag.setCheckable(True)
        self.actionTag.setObjectName("actionTag")
        self.actionFile = QtWidgets.QAction(MainWindow)
        self.actionFile.setCheckable(True)
        self.actionFile.setObjectName("actionFile")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.menuLog.addAction(self.actionStart)
        self.menuLog.addAction(self.actionStop)
        self.menuLog.addAction(self.actionPause)
        self.menuLog.addAction(self.actionContinue)
        self.menuLog.addSeparator()
        self.menuLog.addAction(self.actionOpenFile)
        self.menuLog.addAction(self.actionOpenLog)
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionDisconnect)
        self.menuFile.addAction(self.actionRe_Connect)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuLog.menuAction())
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionOtherSave)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionClear)
        self.menuEdit.addAction(self.actionClearCache)
        self.menuEdit.addAction(self.actionClear_All)
        self.menuFilter.addAction(self.actionBy_level)
        self.menuFilter.addAction(self.actionBy)
        self.menuFilter.addAction(self.actionBy_function)
        self.menuFilter.addAction(self.actionBy_file)
        self.menuFilter.addAction(self.actionDefine)
        self.menuView.addAction(self.actionFind)
        self.menuView.addAction(self.actionFind_All)
        self.menuView.addSeparator()
        self.menuView.addAction(self.menuFilter.menuAction())
        self.menuTools.addAction(self.actionOptions)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionFast_cmd)
        self.menuTools.addAction(self.actionClolor)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionIPC_parse)
        self.menuShow.addAction(self.actionTime)
        self.menuShow.addAction(self.actionTag)
        self.menuShow.addAction(self.actionFile)
        self.menuOption.addAction(self.menuShow.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuOption.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionRe_Connect)
        self.toolBar.addAction(self.actionDisconnect)
        self.toolBar.addAction(self.menuShow.menuAction())
        self.toolBar.addAction(self.actionIPC_parse)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.buttonSend.setText(_translate("MainWindow", "发送"))
        self.menuFile.setTitle(_translate("MainWindow", "文件"))
        self.menuLog.setTitle(_translate("MainWindow", "日志"))
        self.menuEdit.setTitle(_translate("MainWindow", "编辑"))
        self.menuView.setTitle(_translate("MainWindow", "查看"))
        self.menuFilter.setTitle(_translate("MainWindow", "筛选"))
        self.menuTools.setTitle(_translate("MainWindow", "工具"))
        self.menuOption.setTitle(_translate("MainWindow", "选项卡"))
        self.menuShow.setTitle(_translate("MainWindow", "显示"))
        self.menuWindow.setTitle(_translate("MainWindow", "窗口"))
        self.menuHelp.setTitle(_translate("MainWindow", "帮助"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionOpen.setText(_translate("MainWindow", "打开"))
        self.actionDisconnect.setText(_translate("MainWindow", "断开"))
        self.actionRe_Connect.setText(_translate("MainWindow", "重连"))
        self.actionImport.setText(_translate("MainWindow", "导入"))
        self.actionExport.setText(_translate("MainWindow", "导出"))
        self.actionSave.setText(_translate("MainWindow", "保存"))
        self.actionOtherSave.setText(_translate("MainWindow", "另存为"))
        self.actionStart.setText(_translate("MainWindow", "开始"))
        self.actionStop.setText(_translate("MainWindow", "停止"))
        self.actionPause.setText(_translate("MainWindow", "暂停"))
        self.actionContinue.setText(_translate("MainWindow", "继续"))
        self.actionOpenFile.setText(_translate("MainWindow", "打开文件夹"))
        self.actionOpenLog.setText(_translate("MainWindow", "打开日志"))
        self.actionCopy.setText(_translate("MainWindow", "复制"))
        self.actionPaste.setText(_translate("MainWindow", "粘贴"))
        self.actionCut.setText(_translate("MainWindow", "剪切"))
        self.actionClear.setText(_translate("MainWindow", "清屏"))
        self.actionClearCache.setText(_translate("MainWindow", "清缓存"))
        self.actionClear_All.setText(_translate("MainWindow", "清屏和缓存"))
        self.actionFind.setText(_translate("MainWindow", "查找"))
        self.actionFind_All.setText(_translate("MainWindow", "查找所有"))
        self.actionOptions.setText(_translate("MainWindow", "选项"))
        self.actionFast_cmd.setText(_translate("MainWindow", "快速指令"))
        self.actionClolor.setText(_translate("MainWindow", "颜色"))
        self.actionIPC_parse.setText(_translate("MainWindow", "IPC解析"))
        self.actionBy_level.setText(_translate("MainWindow", "按等级"))
        self.actionBy.setText(_translate("MainWindow", "按标签"))
        self.actionBy_function.setText(_translate("MainWindow", "按函数"))
        self.actionBy_file.setText(_translate("MainWindow", "按文件"))
        self.actionDefine.setText(_translate("MainWindow", "自定义"))
        self.actionTime.setText(_translate("MainWindow", "时间"))
        self.actionTag.setText(_translate("MainWindow", "标签"))
        self.actionFile.setText(_translate("MainWindow", "等级"))
        self.actionNew.setText(_translate("MainWindow", "新建"))
