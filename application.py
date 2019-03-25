import sys, csv, os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from collections import defaultdict as dfd

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd

DATA = None

class App(QWidget):
    def __init__(self):
        super(App, self).__init__()
        self.title = "FOSSEE SCREENING TASK 2"
        self.upleft, self.downleft, self.upright, self.downright = 40, 800, 60, 800
        # self.loadCsv()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.upleft, self.upright, self.downleft, self.downright)

        #for plot:
        self.plot = QAction('&Plot', self)
        self.plot.setShortcut('Ctrl+Shift+P')


        #Make MenuBar
        self.bar = QMainWindow(self).menuBar()
        self.file = self.bar.addMenu('File')
        self.edit = self.bar.addMenu('Edit')
        self.bar.addAction(self.plot)

        #For File Option
        self.load_action = QAction('&Load', self)
        self.load_action.setShortcut('Ctrl+O')
        self.file.addAction(self.load_action)

        self.add_data = self.file.addMenu('Add Data')
        self.new_column = QAction('New Column', self)
        self.new_column.setShortcut('Ctrl+Shift+C')
        self.new_row = QAction('New Row', self)
        self.new_row.setShortcut('Ctrl+Shift+R')
        self.add_data.addAction(self.new_column)
        self.add_data.addAction(self.new_row)

        self.save_action = self.file.addMenu('Save')
        self.save = QAction('Save', self)
        self.save.setShortcut('Ctrl+S')
        self.new_save = QAction('Save As', self)
        self.new_save.setShortcut('Ctrl+Shift+S')
        self.save_action.addAction(self.save)
        self.save_action.addAction(self.new_save)



        #For Edit Option
        self.edit_action = QAction('&Edit', self)
        self.edit_action.setShortcut('Ctrl+E')
        self.edit.addAction(self.edit_action)


        #command for File menu-options
        self.fileOPened = False
        self.load_action.triggered.connect(self.loadCsv)
        self.save.triggered.connect(lambda: self.saveData(True))
        self.new_save.triggered.connect(lambda: self.saveData(False))
        self.new_column.triggered.connect(lambda: self.addData('Col'))
        self.new_row.triggered.connect(lambda: self.addData('Row'))

        #command for Edit menu-options
        self.edit_action.triggered.connect(self.editData)

        #command for Plot
        self.plot.triggered.connect(self.plotData)


        # self.createTable()
        # self.loadbtn = QPushButton(self)
        # self.loadbtn.setText("Load the csv file")
        # self.loadbtn.clicked.connect(self.loadCsv)

        self.layout = QVBoxLayout()
        # self.layout.addWidget(self.loadbtn)
        self.layout.addWidget(self.bar)
        # self.layout.addWidget(self.twig)
        self.setLayout(self.layout)
        self.show()

    def loadCsv(self):
        global DATA
        self.filename = (QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)'))[0]
        if self.filename != '':
            fileinput = open(self.filename, 'r')
            self.data = list(csv.reader(fileinput))
            DATA = self.data
            self.row_size = len(self.data)
            self.column_size = max([len(self.data[0]), len(self.data[1]), len(self.data[2])])
            if not self.fileOPened:
                self.fileOPened = True
                self.createTable(True)
            else:
                self.createTable(False)

    def createTable(self, flag):
        if flag:
            self.twig = QTableWidget()
        else:
            self.twig.setRowCount(0)
        self.twig.setRowCount(self.row_size)
        self.twig.setColumnCount(self.column_size)
        for i in range(self.row_size):
            for j in range(self.column_size):
                try:
                    point = str(self.data[i][j])
                except:
                    point = ""
                self.twig.setItem(i, j, QTableWidgetItem(point))
                self.twig.item(i, j).setFlags(QtCore.Qt.ItemIsEnabled)
        self.twig.move(0, 0)
        self.layout.addWidget(self.twig)
        self.setLayout(self.layout)
        self.show()

    def editData(self):
        # self.twig = QTableWidget()
        # self.twig.setRowCount(self.row_size)
        # self.twig.setColumnCount(self.column_size)
        if not self.fileOPened:
            QMessageBox.about(self, "Error", "First Load a .csv File")
        else:
            for i in range(self.row_size):
                for j in range(self.column_size):
                    self.twig.setItem(i, j, QTableWidgetItem(self.twig.item(i, j).text()))

    def saveData(self, opt):
        #give a pop-up to ask if want to save change in the already existing file
        #or want to save to another file compeletely
        if not self.fileOPened:
            QMessageBox.about(self, "Error", "First Load a .csv File")
        else:
            data = []
            for i in range(self.row_size):
                rowww = []
                for j in range(self.column_size):
                    rowww.append(self.twig.item(i, j).text())
                data.append(rowww) #data stores all the data row-wise
            if opt:
                #Will save in Loaded file itself
                with open(self.filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(data)
            else:
                #Will save in new File
                path = QFileDialog.getSaveFileName(self, 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)')
                if path[0]=='':
                    QMessageBox.about(self, "Error", "Select a Path")
                else:
                    with open(path[0], 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerows(data)

    def addData(self, flag):
        if not self.fileOPened:
            QMessageBox.about(self, "Error", "First Load a .csv File")
        else:
            if flag=='Col':
                self.twig.setColumnCount(self.column_size+1)
                for i in range(self.row_size):
                    self.twig.setItem(i, self.column_size, QTableWidgetItem(""))
                self.column_size += 1
            elif flag=='Row':
                self.twig.setRowCount(self.row_size+1)
                for i in range(self.column_size):
                    self.twig.setItem(self.row_size, i, QTableWidgetItem(""))
                self.row_size += 1

    def closeEvent(self, event):
        self.reference = None

    def plotData(self):
        if not self.fileOPened:
            QMessageBox.about(self, "Error", "First Load a .csv File")
        elif len(self.data[0]) < 2:
            QMessageBox.about(self, "Error", "Please select a DataSet which has more than One Column!!!")
        else:
            self.reference = Plot_Data()
            self.reference.show()


class Plot_Data(QWidget):
    def __init__(self):
        super(Plot_Data, self).__init__()
        self.title = "FOSSEE SCREENING TASK 2 - Ploting Part"
        self.upleft, self.downleft, self.upright, self.downright = 500, 900, 100, 900
        self.initui()

    def initui(self):
        global DATA
        self.setWindowTitle(self.title)
        self.setGeometry(self.upleft, self.upright, self.downleft, self.downright)


        self.plot_bar = QMainWindow(self).menuBar()
        self.plot_file = self.plot_bar.addMenu('File')
        self.plot_save_action = QAction('&Save as png', self)
        self.plot_save_action.triggered.connect(self.savePNG)
        # self.plot_save_action.setShortcut('Ctrl+S')
        self.plot_file.addAction(self.plot_save_action)


        self.xl = QLabel("Select the column for X-Axis:")
        self.yl = QLabel("Select the column for Y-Axis:")
        self.poption = QLabel("Select the Plotting Style:")
        self.xbox = QComboBox()
        self.ybox = QComboBox()
        self.pbox = QComboBox()
        self.btn = QPushButton("PLOT THE GRAPH")


        #defaultdict to store the data in form of
        # dictionary so that it is easy to access
        # column wise
        self.dd = dfd(list)

        for i in range(len(DATA[0])):
            self.xbox.addItem(DATA[0][i])
            self.ybox.addItem(DATA[0][i])
            self.dd[DATA[0][i]]

        for i in range(1, len(DATA)):
            for j in range(len(DATA[i])):
                try:self.dd[DATA[0][j]].append( float(DATA[i][j]))
                except:pass

##        print(self.dd)

        self.pbox.addItem("Scatter Points")
        self.pbox.addItem("Scatter Points with Smooth Lines")
        self.pbox.addItem("Plot Lines")


        self.tabs = QTabWidget()
        self.tabs.resize(500, 500)


        self.v_box = QVBoxLayout()
        self.v_box.addWidget(self.plot_bar)
        self.v_box.addWidget(self.xl)
        self.v_box.addWidget(self.xbox)
        self.v_box.addWidget(self.yl)
        self.v_box.addWidget(self.ybox)
        self.v_box.addWidget(self.poption)
        self.v_box.addWidget(self.pbox)
        self.v_box.addWidget(self.btn)
        self.v_box.addWidget(self.tabs)

        self.tab1, self.tab2, self.tab3 = None, None, None
        self.t1x, self.t1y, self.t2x, self.t2y, self.t3x, self.t3y = None, None, None, None, None, None

        self.btn.clicked.connect(self.fig)

        self.setLayout(self.v_box)

    def fig(self):
        if self.xbox.currentText() == self.ybox.currentText():
            QMessageBox.about(self, "Error", "Select different Column's for X and Y axes!!!")
        else:
            if self.pbox.currentText()=="Scatter Points":
                if self.tab1 == None:

                    self.tab1 = QWidget()
                    self.tab1.setObjectName("tab1")
                    self.tab1.layout = QVBoxLayout(self)
                    self.tabs.addTab(self.tab1, "Scatter Point")
                    self.tabs.setCurrentWidget(self.tab1)


                    self.figure1 = plt.figure(0)
                    self.canvas1 = FigureCanvas(self.figure1)
                    self.figure1.clear()
                    self.ax = self.figure1.add_subplot(111)

                    self.ax.set_title(r"$\bf{" + self.pbox.currentText() + "}$")
                    self.ax.set_xlabel(r"$\bf{" + self.xbox.currentText() + "}$")
                    self.ax.set_ylabel(r"$\bf{" + self.ybox.currentText() + "}$")

                    # self.ax.xaxis.label.set_color("green")
                    # self.ax.yaxis.label.set_color("blue")

                    self.ax.scatter(self.dd[self.xbox.currentText()], self.dd[self.ybox.currentText()])
                    self.t1x = self.xbox.currentText()
                    self.t1y = self.ybox.currentText()

                    self.canvas1.draw()

                    self.tab1.layout.addWidget(self.canvas1)
                    self.tab1.setLayout(self.tab1.layout)
                else:
                    if self.xbox.currentText()!=self.t1x or self.ybox.currentText()!=self.t1y:
                        self.tabs.setCurrentWidget(self.tab1)
                        for i in reversed(range(self.tab1.layout.count())):
                            self.tab1.layout.itemAt(i).widget().setParent(None)


                        self.figure1 = plt.figure(0)
                        self.canvas1 = FigureCanvas(self.figure1)
                        self.figure1.clear()
                        self.ax = self.figure1.add_subplot(111)

                        self.ax.set_title(r"$\bf{" + self.pbox.currentText() + "}$")
                        self.ax.set_xlabel(r"$\bf{" + self.xbox.currentText() + "}$")
                        self.ax.set_ylabel(r"$\bf{" + self.ybox.currentText() + "}$")

                        self.ax.scatter(self.dd[self.xbox.currentText()], self.dd[self.ybox.currentText()])

                        self.t1x = self.xbox.currentText()
                        self.t1y = self.ybox.currentText()

                        self.canvas1.draw()

                        self.tab1.layout.addWidget(self.canvas1)
                        self.tab1.setLayout(self.tab1.layout)
                    else:
                        self.tabs.setCurrentWidget(self.tab1)

            elif self.pbox.currentText()=="Scatter Points with Smooth Lines":
                if self.tab2 == None:
                    self.tab2 = QWidget()
                    self.tab2.setObjectName("tab2")
                    self.tab2.layout = QVBoxLayout(self)
                    self.tabs.addTab(self.tab2, "Scatter Points with Smooth Lines")
                    self.tabs.setCurrentWidget(self.tab2)

                    self.figure2 = plt.figure(1)
                    self.canvas2 = FigureCanvas(self.figure2)
                    self.figure2.clear()
                    self.bx = self.figure2.add_subplot(111)

                    self.bx.set_title(r"$\bf{" + self.pbox.currentText() + "}$")
                    self.bx.set_xlabel(r"$\bf{" + self.xbox.currentText() + "}$")
                    self.bx.set_ylabel(r"$\bf{" + self.ybox.currentText() + "}$")


                    #smothening part
##                    self.x = np.array([float(i) for i in self.dd[self.xbox.currentText()]])
##                    self.y = np.array([float(i) for i in self.dd[self.ybox.currentText()]])

                    self.x = np.array(self.dd[self.xbox.currentText()])
                    self.y = np.array(self.dd[self.ybox.currentText()])
                    
                    print(self.x)
                    print(self.y)
                    
                    self.x_new = np.linspace(self.x.min(), self.x.max(), 500)
                    print("first")
                    self.f = interp1d(self.x, self.y, kind="quadratic") #this line is failing
                    print("second")
                    self.y_smooth = self.f(self.x_new)


                    self.bx.plot(self.x_new, self.y_smooth)
                    self.bx.scatter(self.x, self.y)
                    self.t2x = self.xbox.currentText()
                    self.t2y = self.ybox.currentText()

                    self.canvas2.draw()

                    self.tab2.layout.addWidget(self.canvas2)
                    self.tab2.setLayout(self.tab2.layout)
                else:
                    if self.xbox.currentText() != self.t2x or self.ybox.currentText() != self.t2y:
                        self.tabs.setCurrentWidget(self.tab2)
                        # for i in reversed(range(self.tab2.layout.count())):
                        #     self.tab2.layout.itemAt(i).widget().setParent(None)
                        #
                        # self.figure2 = plt.figure(1)
                        # self.canvas2 = FigureCanvas(self.figure2)
                        # self.figure2.clear()
                        # self.bx = self.figure2.add_subplot(111)
                        #
                        # self.bx.set_title(r"$\bf{" + self.pbox.currentText() + "}$")
                        # self.bx.set_xlabel(r"$\bf{" + self.xbox.currentText() + "}$")
                        # self.bx.set_ylabel(r"$\bf{" + self.ybox.currentText() + "}$")
                        #
                        # # smothening part
                        # self.x = np.array([int(i) for i in self.dd[self.xbox.currentText()]])
                        # self.y = np.array([int(i) for i in self.dd[self.ybox.currentText()]])
                        #
                        # self.x_new = np.linspace(min(self.x), max(self.x), 500)
                        # self.f = interp1d(self.x, self.y, kind='quadratic')
                        # self.y_smooth = self.f(self.x_new)
                        #
                        # self.bx.plot(self.x_new, self.y_smooth)
                        # self.bx.scatter(self.x, self.y)
                        # self.t2x = self.xbox.currentText()
                        # self.t2y = self.ybox.currentText()
                        #
                        # self.canvas2.draw()
                        #
                        # self.tab2.layout.addWidget(self.canvas2)
                        # self.tab2.setLayout(self.tab2.layout)
                    else:
                        self.tabs.setCurrentWidget(self.tab2)

            elif self.pbox.currentText()=="Plot Lines":
                if self.tab3 == None:
                    self.tab3 = QWidget()
                    self.tab3.setObjectName("tab3")
                    self.tab3.layout = QVBoxLayout(self)
                    self.tabs.addTab(self.tab3, "Line Plot")
                    self.tabs.setCurrentWidget(self.tab3)

                    self.figure3 = plt.figure(2)
                    self.canvas3 = FigureCanvas(self.figure3)
                    self.figure3.clear()
                    self.cx = self.figure3.add_subplot(111)

                    self.cx.set_title(r"$\bf{" + self.pbox.currentText() + "}$")
                    self.cx.set_xlabel(r"$\bf{" + self.xbox.currentText() + "}$")
                    self.cx.set_ylabel(r"$\bf{" + self.ybox.currentText() + "}$")

                    self.cx.plot(self.dd[self.xbox.currentText()], self.dd[self.ybox.currentText()])
                    self.t3x = self.xbox.currentText()
                    self.t3y = self.ybox.currentText()

                    self.canvas3.draw()

                    self.tab3.layout.addWidget(self.canvas3)
                    self.tab3.setLayout(self.tab3.layout)
                else:
                    if self.xbox.currentText()!=self.t3x or self.ybox.currentText()!=self.t3y:
                        self.tabs.setCurrentWidget(self.tab3)

                        for i in reversed(range(self.tab3.layout.count())):
                            self.tab3.layout.itemAt(i).widget().setParent(None)


                        self.figure3 = plt.figure(2)
                        self.canvas3 = FigureCanvas(self.figure3)
                        self.figure3.clear()
                        self.cx = self.figure3.add_subplot(111)

                        self.cx.set_title(r"$\bf{" + self.pbox.currentText() + "}$")
                        self.cx.set_xlabel(r"$\bf{" + self.xbox.currentText() + "}$")
                        self.cx.set_ylabel(r"$\bf{" + self.ybox.currentText() + "}$")

                        self.cx.plot(self.dd[self.xbox.currentText()], self.dd[self.ybox.currentText()])
                        self.t3x = self.xbox.currentText()
                        self.t3y = self.ybox.currentText()

                        self.canvas3.draw()

                        self.tab3.layout.addWidget(self.canvas3)
                        self.tab3.setLayout(self.tab3.layout)
                    else:
                        self.tabs.setCurrentWidget(self.tab3)

    def savePNG(self):
        if self.tabs.currentIndex() == -1:
            QMessageBox.about(self, "Error", "First Plot a Graph to save as Image in .png format")
        else:
            print(self.tabs.currentWidget().objectName())


app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())
