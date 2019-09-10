from database import Database
import os
from PyQt4 import QtCore,QtGui
from serving import Serving
import sys

def cls():
    os.system("clear")


class MainApp(QtGui.QApplication):
    def __init__(self,cmdArgs = [], title=""):
        QtGui.QApplication.__init__(self,cmdArgs)

        self.title = title

        self.startWindow = StartWindow(self.title)

class StartWindow(QtGui.QWidget):
    def __init__(self,title=""):
        super(QtGui.QWidget,self).__init__()

        self.show()


if __name__ == "__main__":
    database = Database(dirname = ".foods",filename="foods.dat",fieldname="name")

    app = MainApp(title="Diet")
    app.setStyleSheet(open("window.css").read())

    sys.exit(app.exec_())
