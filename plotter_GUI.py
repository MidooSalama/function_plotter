import sys
from PySide2 import QtWidgets, QtCore, QtGui
import random

import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure



class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)



class plotterApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function plotter")
        self.setGeometry(300, 400, 600, 600)



        # nData = 50
        # self.xData = list(range(nData))
        # self.yData = [random.randint(0, 10) for i in range(nData)]
        # self.canvas.axes.plot(self.xData, self.yData, 'r')
        # self.canvas.draw()
        # output graph
        self.canvas = MplCanvas(self, 5, 4, 100)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        # input data Container
        self.createDataGroupBox()
        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.toolbar, 0, 0)
        grid.addWidget(self.canvas, 1, 0)
        grid.addWidget(self.dataGroupBox, 2, 0)
        widget = QtWidgets.QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)



    def drawGraph(self, xData, yData):
        self.canvas.axes.plot(xData, yData, 'r')
        self.canvas.draw()



    def createDataGroupBox(self):
        self.dataGroupBox = QtWidgets.QGroupBox("curve input data", self)
        # self.dataGroupBox.setFont(QtGui.QFont("Sanserif", 13))
        grid = QtWidgets.QGridLayout()

        self.label_function = QtWidgets.QLabel("function",self)
        grid.addWidget(self.label_function, 0, 0)

        self.lineEdit_function = QtWidgets.QLineEdit(self)
        self.lineEdit_function.setPlaceholderText("function")
        grid.addWidget(self.lineEdit_function, 0, 1, 1, -1)

        self.label_xMin = QtWidgets.QLabel("X min",self)
        grid.addWidget(self.label_xMin, 1, 0)

        self.lineEdit_xMin = QtWidgets.QLineEdit(self)
        self.lineEdit_xMin.setPlaceholderText("X min")
        grid.addWidget(self.lineEdit_xMin, 1, 1)

        self.label_xMax = QtWidgets.QLabel("X max",self)
        grid.addWidget(self.label_xMax, 1, 2)

        self.lineEdit_xMax = QtWidgets.QLineEdit(self)
        self.lineEdit_xMax.setPlaceholderText("X max")
        grid.addWidget(self.lineEdit_xMax, 1, 3)

        self.pushButton_plot = QtWidgets.QPushButton("plot",self)
        grid.addWidget(self.pushButton_plot, 1, 4)

        self.dataGroupBox.setLayout(grid)


    def setPlotButton(self):
        plotBtn = QtWidgets.QPushButton("Plot", self)
        plotBtn.move(0, 0)
        plotBtn.clicked.connect(self.plot)

    def plot(self):
        message = QtWidgets.QMessageBox.about(self, "plotting", "plot the curve")
        # message.setText("plotting")
        # message.show()

    def center(self):
        frame = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame.moveCenter(centerPoint)
        self.move(frame.topLeft())

    def createStatusBar(self):
        self.myStatusBar = QtWidgets.QStatusBar()
        self.myStatusBar.showMessage("That is the status bar")
        self.setStatusBar(self.myStatusBar)



app = QtWidgets.QApplication(sys.argv)
myApp = plotterApp()
myApp.show()
app.exec_()