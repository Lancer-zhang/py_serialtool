import matplotlib

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


# class Myplot for plotting with matplotlib
class Myplot(FigureCanvas):
    def __init__(self, parent=None, width=5, height=3, dpi=100):
        # normalized for 中文显示和负号
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        # new figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # activate figure window
        # super(Plot_dynamic,self).__init__(self.fig)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        # self.fig.canvas.mpl_connect('button_press_event', self)
        # sub plot by self.axes
        self.axes = self.fig.add_subplot(111)
        # initial figure
        self.compute_initial_figure()

        # size policy
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class dynamic_fig(Myplot):
    def __init__(self, *args, **kwargs):
        Myplot.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        counts = [1, 10]
        delay_t = [0, 1]
        self.axes.plot(delay_t, counts, '-ob')
        self.axes.set_title("signals")
        self.axes.set_xlabel("delay(s)")
        self.axes.set_ylabel("counts")

