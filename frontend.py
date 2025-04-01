from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QCheckBox, QWidget, QComboBox, QLabel, QPushButton, QTabWidget,QStackedWidget,QScrollArea,QSizePolicy, QPlainTextEdit,QTableWidget,QHBoxLayout, QFrame
import complementos as cp
import backend as be

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #CONSIDERACIONES DE LA VENTANA PRINCIPAL
        self.setWindowTitle("Gestión de finanzas personales") #Crea la ventana principal
        self.setGeometry(100, 100, 700, 500) #Valores iniciales del tamaño de la pestaña sin maximizar
        self.widget_principal = QStackedWidget() #Widget que permite intercambiar entre widgets
        self.setCentralWidget(self.widget_principal) #Hace que el widget de las pestañas sea el principal


        #AGREGAR LAS PÁGINAS CREADAS
        #Instanciar las páginas
        self.home = Home(self.widget_principal)
        self.notas = GestionNotas(self.widget_principal)
        self.paginas = [self.home, self.notas] #Colocarlas en la lista para bucle posterior

        #Agregarlas a QstackedWidget
        for pagina in self.paginas:
            self.widget_principal.addWidget(pagina)

        self.widget_principal.setCurrentIndex(0)

class Home(QWidget):
    def __init__(self, widget_principal):
        super().__init__()

        #WIDGET GENERAL DE LA VENTANA
        self.home_ly = QVBoxLayout()
        self.setLayout(self.home_ly)

        #TITUTLO DE LA VENTANA
        self.titular = cp.Titular("Asistente de finanzas")
        self.titular = self.titular.contenedor

        #CONTNEEDOR DE LAS DOS ZONAS EN VENTANA
        self.z_principal = QWidget()
        self.z_principal_ly = QHBoxLayout()
        self.z_principal.setLayout(self.z_principal_ly)

        #ZONA SALDO DE CUENTAS
        self.z_cuentas = QWidget()
        self.z_cuentas.setMaximumWidth(300)
        self.z_cuentas_ly = QVBoxLayout()
        self.z_cuentas.setLayout(self.z_cuentas_ly)

        #ZONA CARTILLAS CUENTAS
        self.z_c_cuentas = QWidget()
        self.z_c_cuentas_ly = QVBoxLayout()
        self.z_c_cuentas.setLayout(self.z_c_cuentas_ly)

        self.z_cuentas_ly.addWidget(self.z_c_cuentas)

        #LÍNEA DIVISORA
        self.division = QFrame()
        self.division.setFrameShape(QFrame.VLine)
        self.division.setFrameShadow(QFrame.Sunken)

        #Botón agregar cuenta
        instancia = cp.BotónEstándar('Agregar cuenta',lambda:be.agregar_cuenta(self))
        self.b_estandar = instancia.b_estandar

        #ZONA ANALISIS DE INFO
        self.z_analisis = QWidget()
        self.z_analisis_ly = QVBoxLayout()
        self.z_analisis.setLayout(self.z_analisis_ly)

        #Agregamos elementos a zona de cuentas
        self.z_cuentas_ly.addStretch()
        self.z_cuentas_ly.addWidget(self.b_estandar)

        #Agregamos las zonas al contenedor
        elementos_n2 = [self.z_cuentas,self.division,self.z_analisis]

        for i in elementos_n2:
            self.z_principal_ly.addWidget(i)

        #Agregamos el título y contenedor
        elementos_n1 = [self.titular, self.z_principal]

        for i in elementos_n1:
            self.home_ly.addWidget(i)



class GestionNotas (QWidget):
    def __init__(self, widget_principal):
        super().__init__()

       