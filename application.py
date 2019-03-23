import sys, csv, os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

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
        if self.filename!='':
            self.fileOPened = True
            fileinput = open(self.filename, 'r')
            self.data = list(csv.reader(fileinput))
            DATA = self.data
            self.row_size = len(self.data)
            self.column_size = max([len(self.data[0]), len(self.data[1]), len(self.data[2])])
            self.createTable()

    def createTable(self):
        self.twig = QTableWidget()
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

        self.xl = QLabel("Select the column for X-Axis:")
        self.yl = QLabel("Select the column for Y-Axis:")
        self.poption = QLabel("Select the Plotting Style:")
        self.xbox = QComboBox()
        self.ybox = QComboBox()
        self.pbox = QComboBox()
        self.btn = QPushButton("PLOT THE GRAPH")

        for i in range(len(DATA[0])):
            self.xbox.addItem(DATA[0][i])
            self.ybox.addItem(DATA[0][i])
        self.pbox.addItem('Plot Scatter Points')
        self.pbox.addItem('Plot Scatter Points with Smooth Lines')
        self.pbox.addItem('Plot Lines')


        self.tabs = QTabWidget()
        self.tabs.resize(500, 500)


        self.v_box = QVBoxLayout()
        self.v_box.addWidget(self.xl)
        self.v_box.addWidget(self.xbox)
        self.v_box.addWidget(self.yl)
        self.v_box.addWidget(self.ybox)
        self.v_box.addWidget(self.poption)
        self.v_box.addWidget(self.pbox)
        self.v_box.addWidget(self.btn)
        self.v_box.addWidget(self.tabs)

        self.btn.clicked.connect(self.fig)

        self.setLayout(self.v_box)

    def fig(self):
        print(self.xbox.currentText())


app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())