import sys
from PyQt5.QtWidgets import QApplication
import frontend as fe
import backend as be

#Loop que mantiene abierta la ventana principal
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = fe.MainWindow()
    ventana.show()

    be.crear_bbdd()

    sys.exit(app.exec_())