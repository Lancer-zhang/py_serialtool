import sys
import os

path = os.getcwd()
sys.path.append(path + '\\src')
sys.path.append(path + '\\ui')
sys.path.append(path + '\\lib')
sys.path.append(path + '\\config')

from PyQt5.QtWidgets import QApplication, QMainWindow
import mainwindowhandler as UI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = UI.MyMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
