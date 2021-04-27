from PyQt5 import QtWidgets
from sys import argv
from normal_mode import NormalModeWindow


def application():
    app = QtWidgets.QApplication(argv)
    normal_mode = NormalModeWindow()

    normal_mode.show()
    exit(app.exec_())


if __name__ == '__main__':
    application()