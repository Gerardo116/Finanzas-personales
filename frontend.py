from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QCheckBox, QWidget, QComboBox, QLabel, QPushButton, QTabWidget,QStackedWidget,QScrollArea,QSizePolicy, QPlainTextEdit,QTableWidget,QHBoxLayout, QFrame
import complementos as cp
import backend as be

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #CONSIDERACIONES DE LA VENTANA PRINCIPAL
        self.setWindowTitle("Gestión de finanzas personales") #Crea la ventana principal
        self.adjustSize()
        self.setMinimumSize(1000,500) #Valores iniciales del tamaño de la pestaña sin maximizar
        self.widget_principal = QStackedWidget() #Widget que permite intercambiar entre widgets
        self.setCentralWidget(self.widget_principal) #Hace que el widget de las pestañas sea el principal


        #AGREGAR LAS PÁGINAS CREADAS
        #Instanciar las páginas
        self.home = Home(self.widget_principal)
        self.proyectado = Proyectado(self.widget_principal,self.home)
        self.paginas = [self.home, self.proyectado] #Colocarlas en la lista para bucle posterior

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

        #ZONA DE BOTONES SUPERIORES
        self.z_otros = QWidget()
        self.z_otros.setMaximumHeight(70)
        self.z_otros_ly = QHBoxLayout()
        self.z_otros.setLayout(self.z_otros_ly)

        self.b_proyectado = cp.BotónEstándar('Proyectados',lambda: be.ir_proyectado(widget_principal)).b_alt2
        self.b_analiticas = cp.BotónEstándar('Analíticas',lambda: be.ir_proyectado(widget_principal)).b_alt2


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

        #Mantenedor de cuentas
        be.cargar_saldos(self)

        #ZONA ANALISIS DE INFO
        self.z_analisis = QWidget()
        self.z_analisis_ly = QVBoxLayout()
        self.z_analisis.setLayout(self.z_analisis_ly)

        self.registros = QTableWidget()
        self.registros.verticalHeader().setVisible(False)
        self.registros.setEditTriggers(QTableWidget.NoEditTriggers)
        self.registros.resizeColumnsToContents()
        be.actualizar_tabla_registros(self)
        self.b_nuevo_registro = cp.BotónEstándar('Nuevo registro', lambda: be.nuevo_registro(self))
        self.b_nuevo_registro = self.b_nuevo_registro.b_estandar

        self.boton_eliminar_registro = cp.BotónEstándar('Eliminar Registro', lambda: be.eliminar_registros(self))
        self.boton_eliminar_registro = self.boton_eliminar_registro.b_alt1


        #Agregamos elementos a la zona de botones superiores
        elementos_superiores = [self.b_proyectado, self.b_analiticas]

        for i in elementos_superiores:
            self.z_otros_ly.addWidget(i)

        #Agregamos elementos a la zona de análisis
        elementos_analisis = [self.registros,self.b_nuevo_registro,self.boton_eliminar_registro]

        for i in elementos_analisis:
            self.z_analisis_ly.addWidget(i)

        #Agregamos elementos a zona de cuentas
        self.z_cuentas_ly.addStretch()
        self.z_cuentas_ly.addWidget(self.b_estandar)

        #Agregamos las zonas al contenedor
        elementos_n2 = [self.z_cuentas,self.division,self.z_analisis]

        for i in elementos_n2:
            self.z_principal_ly.addWidget(i)

        #Agregamos el título y contenedor
        elementos_n1 = [self.titular, self.z_otros, self.z_principal]

        for i in elementos_n1:
            self.home_ly.addWidget(i)



class Proyectado(QWidget):
    def __init__(self, widget_principal,widget_home):
        super().__init__()
        self.widget_home = widget_home
        self.widget_principal = widget_principal
        self.ly = QVBoxLayout()
        self.setLayout(self.ly)

        self.navegacion = cp.Barra_Nav('Ingresos/Egresos Proyectados', self.widget_principal)
        self.tabla_proyectados = QTableWidget()
        self.tabla_proyectados.verticalHeader().setVisible(False)
        self.tabla_proyectados.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_proyectados.resizeColumnsToContents()
        be.actualizar_tabla_proyect(self)
        self.b_registro = cp.BotónEstándar('Nuevo Registro',lambda: be.nuevo_registro_proyect(self)).b_estandar
        self.b_eliminar = cp.BotónEstándar('Eliminar Registro',lambda: be.eliminar_registros_proyect(self)).b_alt1
        self.b_cometer_registros = cp.BotónEstándar('Cometer registros',lambda: be.cometer_registros(self.widget_home,self)).b_alt3
        self.b_cometer_registros_elegidos = cp.BotónEstándar('Cometer registros (Periodo elegido)',be.prueba).b_alt3



        elementos = [self.navegacion, self.tabla_proyectados,self.b_registro, self.b_eliminar, self.b_cometer_registros, self.b_cometer_registros_elegidos]

        for i in elementos:
            self.ly.addWidget(i)

       