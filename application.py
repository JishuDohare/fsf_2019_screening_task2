import sys, csv
from PyQt5.QtWidgets import *


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "FOSSEE SCREENING TASK 2"
        self.upleft, self.downleft, self.upright, self.downright = 0, 800, 0, 800
        self.initUI()
        self.filename = "C:\\Users\\LENOVO\\Desktop\\data.csv"

    def loadCsv(self, filename):
        with open(filename, 'r') as fileinput:
            for row in csv.reader(fileinput):
                print(row)

    def on_pushButtonLoad_clicked(self):
        self.loadCsv(self.fileName)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.upleft, self.upright, self.downleft, self.downright)

        # self.createTable()
        self.loadbtn = QPushButton(self)
        self.loadbtn.setText("Load the csv file")
        self.loadbtn.clicked.connect(self.on_pushButtonLoad_clicked)

        self.layout = QVBoxLayout()
        # self.layout.addWidget(self.twig)
        self.layout.addWidget(self.loadbtn)
        self.setLayout(self.layout)
        self.show()


    def createTable(self):
        self.twig = QTableWidget()
        self.twig.setRowCount(5)
        self.twig.setColumnCount(5)
        for i in range(5):
            for j in range(5):
                point = "Cell ("+str(i+1)+", "+str(j+1)+")"
                self.twig.setItem(i, j, QTableWidgetItem(point))
        self.twig.move(0, 0)


app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())