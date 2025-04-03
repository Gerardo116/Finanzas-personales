import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets, QtCore
import frontend as fe
import backend as be

#Loop que mantiene abierta la ventana principal
if __name__ == "__main__":
    
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    ventana = fe.MainWindow()
    ventana.show()
    
    sys.exit(app.exec_())