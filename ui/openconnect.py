# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'openconnect.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(476, 457)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(6, 0, 461, 451))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonNew = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonNew.sizePolicy().hasHeightForWidth())
        self.pushButtonNew.setSizePolicy(sizePolicy)
        self.pushButtonNew.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonNew.setAutoFillBackground(False)
        self.pushButtonNew.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.pushButtonNew.setObjectName("pushButtonNew")
        self.horizontalLayout.addWidget(self.pushButtonNew)
        self.pushButtonNSave = QtWidgets.QPushButton(self.widget)
        self.pushButtonNSave.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonNSave.setAutoFillBackground(False)
        self.pushButtonNSave.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.pushButtonNSave.setObjectName("pushButtonNSave")
        self.horizontalLayout.addWidget(self.pushButtonNSave)
        self.pushButtonCute = QtWidgets.QPushButton(self.widget)
        self.pushButtonCute.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonCute.setAutoFillBackground(False)
        self.pushButtonCute.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.pushButtonCute.setObjectName("pushButtonCute")
        self.horizontalLayout.addWidget(self.pushButtonCute)
        self.pushButtonCopy = QtWidgets.QPushButton(self.widget)
        self.pushButtonCopy.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonCopy.setAutoFillBackground(False)
        self.pushButtonCopy.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.pushButtonCopy.setObjectName("pushButtonCopy")
        self.horizontalLayout.addWidget(self.pushButtonCopy)
        self.pushButtonPaste = QtWidgets.QPushButton(self.widget)
        self.pushButtonPaste.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonPaste.setAutoFillBackground(False)
        self.pushButtonPaste.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.pushButtonPaste.setObjectName("pushButtonPaste")
        self.horizontalLayout.addWidget(self.pushButtonPaste)
        self.pushButtonDelete = QtWidgets.QPushButton(self.widget)
        self.pushButtonDelete.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonDelete.setAutoFillBackground(False)
        self.pushButtonDelete.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.horizontalLayout.addWidget(self.pushButtonDelete)
        self.pushButtonTrait = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonTrait.sizePolicy().hasHeightForWidth())
        self.pushButtonTrait.setSizePolicy(sizePolicy)
        self.pushButtonTrait.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButtonTrait.setAutoFillBackground(False)
        self.pushButtonTrait.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.pushButtonTrait.setObjectName("pushButtonTrait")
        self.horizontalLayout.addWidget(self.pushButtonTrait)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableWidget = QtWidgets.QTableWidget(self.widget)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setStyleSheet("color: blue;")
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(110)
        self.tableWidget.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButtonConnect = QtWidgets.QPushButton(self.widget)
        self.pushButtonConnect.setObjectName("pushButtonConnect")
        self.horizontalLayout_2.addWidget(self.pushButtonConnect)
        self.pushButtonClose = QtWidgets.QPushButton(self.widget)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.horizontalLayout_2.addWidget(self.pushButtonClose)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "打开"))
        self.pushButtonNew.setText(_translate("Dialog", "新建"))
        self.pushButtonNSave.setText(_translate("Dialog", "另存为"))
        self.pushButtonCute.setText(_translate("Dialog", "剪贴"))
        self.pushButtonCopy.setText(_translate("Dialog", "复制"))
        self.pushButtonPaste.setText(_translate("Dialog", "粘贴"))
        self.pushButtonDelete.setText(_translate("Dialog", "删除"))
        self.pushButtonTrait.setText(_translate("Dialog", "属性"))
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "ID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "名称"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "端口"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "说明"))
        self.pushButtonConnect.setText(_translate("Dialog", "连接"))
        self.pushButtonClose.setText(_translate("Dialog", "关闭"))
