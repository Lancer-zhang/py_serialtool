import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import mainwindowhandler as UI


class global_data:
    level_flag = ['D ']
    rec_show = {'time': True, 'tag': True, 'level': True}
    rec_filter = []
    rec_parse = {}


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = UI.MyMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
