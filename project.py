import sys
from PyQt5 import QtWidgets, QtGui


def window():
    app = QtWidgets.QApplication(sys.argv)

    #to set the tital
    w = QtWidgets.QWidget()
    w.setWindowTitle("PyQt Lessons")

    #To set the label for just txt
    label = QtWidgets.QLabel(w)
    label.setText("Hello World!!!!")
    label.move(200, 20) #co-ordinates of label w.r.t. to window

    #to set image using label
    label2 = QtWidgets.QLabel(w)
    label2.setPixmap(QtGui.QPixmap('pic1.png'))
    label2.move(100, 40)


    #set co-ordinates
    w.setGeometry(500, 400, 500, 400) #(how much from left side of scree, how much from top of the screen, width, height)

    #to display the window
    w.show()
    sys.exit(app.exec_())


window()

# linear, logistic, knn, k-means, neural network
