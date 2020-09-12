import sys
from PySide2 import QtWidgets, QtCore, QtGui
import random
import numpy as np
from decimal import Decimal

import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

import function_calc



class MplCanvas(FigureCanvasQTAgg):
    # This class is for plot widget and figure of the calculated data
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.add_axes(yScale='log')
        super(MplCanvas, self).__init__(fig)



class plotterApp(QtWidgets.QMainWindow):
    # This is the main appliction Class where the whole GUI is built
    def __init__(self):
        super().__init__()
        # set initial window shape
        self.setWindowTitle("Function plotter")
        self.setGeometry(300, 400, 600, 600)

        # create initial figure and toolbar for the plotter
        self.canvas = MplCanvas(self, 5, 4, 100)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.createDataGroupBox() # container for the input data

        # organize the layout of the main parts of the GUI
        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.toolbar, 0, 0)
        grid.addWidget(self.canvas, 1, 0)
        grid.addWidget(self.dataGroupBox, 2, 0)
        widget = QtWidgets.QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)
        self.center()

        # connect signals and slots
        self.pushButton_plot.clicked.connect(self.plotFunction)



    def drawGraph(self, xData, yData):
        # this function takes the x,y data arrays to plot it on the figure directly
        # Inputs:
        #   - xData: Array of input data on the X-axis
        #   - yData: Array of the corresponding data on the Y-axis
        self.canvas.axes.cla()
        self.canvas.axes.plot(xData, yData, 'r')
        self.canvas.draw()

    def plotFunction(self):
        # This function is called on pushbutton click event, it takes the needed arguments from different elemnts in
        # the GUI, making sure of their validity then calculate the function to plot the data, The main function is
        # organised here

        # initialize main input data
        functionString = None
        xMin = None
        xMax = None

        # verify None empty input data
        if self.lineEdit_function.text():
            functionString = self.lineEdit_function.text()
        else:
            QtWidgets.QMessageBox.about(self, "empty Function", "you have to enter a function expression")
            return
        if self.lineEdit_xMin.text() and self.lineEdit_xMax.text():
            xMin = float(Decimal(self.lineEdit_xMin.text()))
            xMax = float(Decimal(self.lineEdit_xMax.text()))
            if xMin >= xMax:
                QtWidgets.QMessageBox.about(self, "Wrong limits", "x min limit should be less than x max limit")
                return
        else:
            QtWidgets.QMessageBox.about(self, "empty X limits", "you have to enter the two X limit values")
            return

        # do the main stuff after checking none empty input data
        if functionString != None and xMin != None and xMax != None:

            # check for Valid input Function Expression
            if(not function_calc.funcStringIsValid(functionString)):
                QtWidgets.QMessageBox.about(self, "Wrong Expression", "Not a valid Expression")
            else:
                # partitioning the complex expression into simple elements  (operators and operands) stored in array
                expressionArray = function_calc.function_parsing(functionString)
                xArray = np.linspace(xMin, xMax, 100)
                yArray = []

                # calculate the function for each x value from the X-axis
                for x in xArray:
                    y = function_calc.calculateExpersion(expressionArray, x)
                    yArray.append(float(y))
                self.drawGraph(xArray, yArray)



    def createDataGroupBox(self):
        # build the container for input data
        self.dataGroupBox = QtWidgets.QGroupBox("curve input data", self)
        grid = QtWidgets.QGridLayout()

        self.label_function = QtWidgets.QLabel("function",self)
        grid.addWidget(self.label_function, 0, 0)

        self.lineEdit_function = QtWidgets.QLineEdit(self)
        self.lineEdit_function.setPlaceholderText("function")
        grid.addWidget(self.lineEdit_function, 0, 1, 1, -1) # make it wider

        self.label_xMin = QtWidgets.QLabel("X min",self)
        grid.addWidget(self.label_xMin, 1, 0)

        self.lineEdit_xMin = QtWidgets.QLineEdit(self)
        self.lineEdit_xMin.setPlaceholderText("X min")
        self.lineEdit_xMin.setValidator(QtGui.QDoubleValidator())
        grid.addWidget(self.lineEdit_xMin, 1, 1)

        self.label_xMax = QtWidgets.QLabel("X max",self)
        grid.addWidget(self.label_xMax, 1, 2)

        self.lineEdit_xMax = QtWidgets.QLineEdit(self)
        self.lineEdit_xMax.setPlaceholderText("X max")
        self.lineEdit_xMax.setValidator(QtGui.QDoubleValidator())
        grid.addWidget(self.lineEdit_xMax, 1, 3)

        self.pushButton_plot = QtWidgets.QPushButton("plot",self)
        grid.addWidget(self.pushButton_plot, 1, 4)

        self.dataGroupBox.setLayout(grid)



    def center(self):
        frame = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame.moveCenter(centerPoint)
        self.move(frame.topLeft())



if __name__ == "__main__":
    # start the main application
    app = QtWidgets.QApplication(sys.argv)
    myApp = plotterApp()
    myApp.show()
    app.exec_()