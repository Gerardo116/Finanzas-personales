from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QInputDialog, QComboBox, QLineEdit, QDialog, QDateEdit
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIntValidator, QDoubleValidator
import backend as be
import pandas as pd
import os

ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_validaciones = os.path.join(ruta_base, "recursos", "validaciones.xlsx")

class Barra_Nav():
    def __init__(self, titulo, elemento_stacked):

        self.widget_principal = elemento_stacked

        self.contenedor = QWidget()
        self.contenedor_layout = QHBoxLayout()
        self.contenedor.setLayout(self.contenedor_layout)

        self.titulo = QLabel(titulo)
        self.titulo.setStyleSheet("""
            background-color: black;
            color: white;
            font-size: 35px;
            font-family: Arial;
            font-weight: bold;
            letter-spacing: 0.5px;
            border-radius: 8px;
            padding: 5px;
        """)

        self.boton_atras = QPushButton('Atrás')
        self.boton_atras.setStyleSheet("""
            background-color: black;
            color: white;
            font-size: 14px;
            font-family: Arial;
            font-weight: bold;
            letter-spacing: 0.5px;
            border-radius: 8px;
            padding: 5px;
        """)

        self.boton_atras.setMaximumWidth(70)
        self.boton_atras.setMaximumHeight(50)
        self.boton_atras.clicked.connect(self.ir_atras)

        elementos = [self.boton_atras, self.titulo]

        for i in elementos:
            self.contenedor_layout.addWidget(i)
    
    def ir_atras(self):
        pg_actual = self.widget_principal.currentIndex()
        self.widget_principal.setCurrentIndex(pg_actual-1)

class Titular():
    def __init__(self, titulo):

        self.contenedor = QWidget()
        self.contenedor_layout = QHBoxLayout()
        self.contenedor.setLayout(self.contenedor_layout)

        self.titulo = QLabel(titulo)
        self.titulo.setStyleSheet("""
            background-color: #003366;
            color: white;
            font-size: 35px;
            font-family: Arial;
            font-weight: bold;
            letter-spacing: 0.5px;
            border-radius: 8px;
            padding: 5px;
        """)

        self.contenedor.setMaximumHeight(65)

        elementos = [self.titulo]

        for i in elementos:
            self.contenedor_layout.addWidget(i)

class BotónEstándar():
    def __init__(self, titulo, funcion):

        self.b_estandar = QPushButton(titulo)
        self.b_estandar.setStyleSheet("""
            background-color: #006400;
            color: white;
            font-size: 14px;
            font-family: Calibri;
            font-weight: bold;
            letter-spacing: 0.5px;
            border-radius: 8px;
            padding: 5px;
        """)
        self.b_estandar.clicked.connect(funcion)
        self.b_estandar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.b_estandar.setMaximumHeight(40)

        self.b_alt1 = QPushButton(titulo)
        self.b_alt1.setStyleSheet("""
            background-color: red;
            color: white;
            font-size: 14px;
            font-family: Calibri;
            font-weight: bold;
            letter-spacing: 0.5px;
            border-radius: 8px;
            padding: 5px;
        """)
        self.b_alt1.clicked.connect(funcion)
        self.b_alt1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.b_alt1.setMaximumHeight(40)

class Cartilla():
    def __init__(self, titulo, saldo):
        
        self.contenedor = QWidget()
        self.contenedor.setStyleSheet("""
        background-color: #FFD700;
        border-radius: 10px;
        """)
        self.contenedor_ly = QVBoxLayout()
        self.contenedor.setLayout(self.contenedor_ly)

        self.titulo = QLabel(titulo)
        self.titulo.setStyleSheet("""
        color: black;
        font-family: Arial;
        font-weight: bold;
        font-size: 20px;
        """)
        self.saldo = QLabel(saldo)
        self.saldo.setStyleSheet("""
        color: black;
        font-family: Arial;
        font-weight: bold;
        font-size: 16px;
        """)

        elementos = [self.titulo, self.saldo]

        for i in elementos:
            self.contenedor_ly.addWidget(i)

class CreaciónCuenta(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.padre = parent

        self.t_cuentas = pd.read_excel(rf'{ruta_validaciones}')
        self.t_cuentas = self.t_cuentas['tipo_cuenta'].dropna().values

        self.t_divisas = pd.read_excel(rf'{ruta_validaciones}')
        self.t_divisas = self.t_divisas['divisas'].dropna().values

        instancia_boton = BotónEstándar('Aceptar',lambda:be.agregar_cartilla(self.padre,self))

        self.setWindowTitle("Creación de cuenta")

        self.cc_layout = QVBoxLayout()
        self.setLayout(self.cc_layout)

        instancia_titulo = Titular('Creación de cuenta')
        self.titulo = instancia_titulo.contenedor

        self.i_t_cuenta = QLabel('Elige el tipo de cuenta')
        self.tipo = QComboBox()

        for i in self.t_cuentas:
            self.tipo.addItem(i)

        self.i_n_cuenta = QLabel('Ingresa un nombre para tu cuenta')
        self.n_cuenta = QLineEdit()

        self.i_s_cuenta = QLabel('Ingresa el saldo inicial de la cuenta')
        self.s_cuenta = QLineEdit()

        self.i_divisas = QLabel('Elige la divisa de la cuenta')
        self.divisas = QComboBox()

        for i in self.t_divisas:
            self.divisas.addItem(str(i))

        self.b_aceptar = instancia_boton.b_estandar


        elementos = [self.titulo, self.i_t_cuenta, self.tipo,self.i_n_cuenta, self.n_cuenta, self.i_s_cuenta, self.s_cuenta, self.i_divisas, self.divisas, self.b_aceptar]

        for i in elementos:
            self.cc_layout.addWidget(i)

class CreacionRegistro(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Nuevo registro")

        self.ly = QVBoxLayout()
        self.setLayout(self.ly)
        self.padre = parent
        validaciones = pd.read_excel(rf'{ruta_validaciones}')

        self.titulo = Titular('Nuevo registro')
        self.titulo = self.titulo.contenedor

        self.t_transaccion = QComboBox()

        for i in validaciones['tipo_transaccion'].dropna().values:
            self.t_transaccion.addItem(i)

        self.monto = QLineEdit()
        self.monto.setValidator(QDoubleValidator())
        self.cuenta_invo = QComboBox()
        nombres = be.traer_nombres()

        for i in nombres:
            self.cuenta_invo.addItem(i)

        self.c_dest = QLineEdit()
        self.categorias = QComboBox()

        for i in validaciones['categorias'].dropna().values:
            self.categorias.addItem(i)

        self.cuenta_dest = QComboBox()
        nombres = be.traer_nombres()

        for i in nombres:
            self.cuenta_dest.addItem(i)

        self.nota = QLineEdit()

        self.fecha = QDateEdit()
        self.fecha.setCalendarPopup(True)
        self.fecha.setDate(QDate.currentDate())

        self.tit_transaccion = QLabel('Elige el tipo de transacción')
        self.tit_monto = QLabel('Introduce el monto')
        self.tit_cuenta = QLabel('Elige la cuenta de origen')
        self.tit_cuenta_dest = QLabel('Elige la cuenta de destino')
        self.tit_categoria = QLabel('Elige la categoría')
        self.tit_nota = QLabel('Agrega una nota')
        self.nota = QLineEdit()
        self.tit_fecha = QLabel('Elige la fecha de transacción')

        self.boton_agregar_registro = BotónEstándar('Agregar Registro',lambda: be.crear_registro(self.padre,self))
        self.boton_agregar_registro = self.boton_agregar_registro.b_estandar


        elementos = [
            self.titulo, 
            self.tit_transaccion, 
            self.t_transaccion,
            self.tit_monto, 
            self.monto, 
            self.tit_cuenta,
            self.cuenta_invo,
            self.tit_cuenta_dest, 
            self.cuenta_dest, 
            self.tit_categoria, 
            self.categorias,
            self.tit_nota,
            self.nota, self.
            tit_fecha, 
            self.fecha, 
            self.boton_agregar_registro,
            ]

        for i in elementos:
            self.ly.addWidget(i)
