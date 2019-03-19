import sys, csv, os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "FOSSEE SCREENING TASK 2"
        self.upleft, self.downleft, self.upright, self.downright = 40, 800, 60, 800
        # self.loadCsv()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.upleft, self.upright, self.downleft, self.downright)

        #Make MenuBar
        self.bar = QMainWindow(self).menuBar()
        self.file = self.bar.addMenu('File')
        self.edit = self.bar.addMenu('Edit')

        #For File Option
        self.load_action = QAction('&Load', self)
        self.load_action.setShortcut('Ctrl+O')

        self.add_data_action = QAction('&Add Data', self)
        self.add_data_action.setShortcut('Ctrl+A')

        self.file.addAction(self.load_action)
        self.file.addAction(self.add_data_action)

        self.save_action = self.file.addMenu('Save')
        self.save = QAction('Save Changes in Current File', self)
        self.save.setShortcut('Ctrl+S')
        self.new_save = QAction('Save as New File', self)
        self.save_action.addAction(self.save)
        self.save_action.addAction(self.new_save)



        #For Edit Option
        self.edit_action = QAction('&Edit', self)
        self.edit_action.setShortcut('Ctrl+E')
        self.edit.addAction(self.edit_action)


        #command for File menu-options
        self.load_action.triggered.connect(self.loadCsv)
        self.save.triggered.connect(lambda: self.saveData(True))
        self.new_save.triggered.connect(lambda: self.saveData(False))

        #command for Edit menu-options
        self.edit_action.triggered.connect(self.editData)


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
        self.filename = (QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)'))[0]
        fileinput = open(self.filename, 'r')
        self.data = list(csv.reader(fileinput))
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
        for i in range(self.row_size):
            for j in range(self.column_size):
                self.twig.setItem(i, j, QTableWidgetItem(self.twig.item(i, j).text()))

    def saveData(self, opt):
        #give a pop-up to ask if want to save change in the already existing file
        #or want to save to another file compeletely
        print(opt)
        pass


app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())