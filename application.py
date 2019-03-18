import sys, csv, os
from PyQt5.QtWidgets import *


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

        # self.createTable()
        self.loadbtn = QPushButton(self)
        self.loadbtn.setText("Load the csv file")
        self.loadbtn.clicked.connect(self.loadCsv)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.loadbtn)
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
        self.twig.move(0, 0)
        self.layout.addWidget(self.twig)
        self.setLayout(self.layout)
        self.show()


app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())