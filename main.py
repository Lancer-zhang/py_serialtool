import sys
import os

path = os.getcwd()
sys.path.append(path + '\\src')
sys.path.append(path + '\\ui')
sys.path.append(path + '\\lib')

from PyQt5.QtWidgets import QApplication, QMainWindow
import mainwindowhandler as UI


class global_data:
    rec_show = {'time': True, 'format': 'asc'}
    send_show = {'format': 'asc'}


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = UI.MyMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
