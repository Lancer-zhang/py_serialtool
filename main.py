import sys
import os
path = os.getcwd()
sys.path.append(path+'\\src')
sys.path.append(path+'\\ui')
sys.path.append(path+'\\lib')

from PyQt5.QtWidgets import QApplication, QMainWindow
import mainwindowhandler as UI


class global_data:
    level_flag = {'d': 'debug', 'debug': 'debug',
                  'i': 'info', 'info': 'info',
                  'w': 'warn', 'warn': 'warn',
                  'e': 'error', 'error': 'error'}
    rec_show = {'time': True, 'tag': True, 'level': True}
    rec_filter = {'level': ['error', 'warn', 'info', 'debug'], 'tag': [], 'content': []}

    plug_tool = {'ipc': False, 'plot': False}


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = UI.MyMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
