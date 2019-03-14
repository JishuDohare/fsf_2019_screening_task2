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
    label.move(100, 20) #co-ordinates of label w.r.t. to window

    #button
    b = QtWidgets.QPushButton(w)
    b.setText("Press")
    b.move(100, 40)

    # to display the window
    w.show()
    sys.exit(app.exec_())


window()
