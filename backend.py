from PyQt5.QtWidgets import QMessageBox
from openpyxl.utils.dataframe import dataframe_to_rows
import complementos as cp
import locale
import sqlite3 as sql
import os

locale.setlocale(locale.LC_NUMERIC, 'es_ES.UTF-8')
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_bbdd = os.path.join(ruta_base, "recursos", "bbdd_general.db")

def prueba():
    print('conectado')


def crear_bbdd():
    conexion = sql.connect(ruta_bbdd)
    cursor = conexion.cursor()
    
    # Creamos la tabla si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS info_cartillas (
    divisa TEXT,
    t_cuenta TEXT,
    nombre TEXT,
    saldo FLOAT
                   
    )
    ''')
    
    conexion.commit()
    conexion.close()

def conectar_bd():
    return sql.connect(ruta_bbdd)

def agregar_cuenta(instancia_home):
    ventana_cc = cp.CreaciónCuenta(parent= instancia_home)
    ventana_cc.show()

def agregar_cartilla(instancia_home, instancia_crear_cuenta):

    conteo = 0
    
    #Diccionario para divisas
    dic_div = {'PEN':"S/.", 'USD':'USD'}

    mensaje_error = QMessageBox(parent=instancia_crear_cuenta)
    mensaje_error.setIcon(QMessageBox.Critical)
    mensaje_error.setText('Revisa los campos')
    mensaje_error.setWindowTitle("Atención")

    #Definición de variables
    #Divisa: No debe ser Seleccionar...
    divisa = instancia_crear_cuenta.divisas.currentText()
    if divisa == "Seleccionar...":
        print('divisa')
        mensaje_error.exec_()
        return
    else:
        pass

    #Tipo de cuenta: No debe ser Seleccionar...
    tipo_cuenta = instancia_crear_cuenta.tipo.currentText()
    if tipo_cuenta == "Seleccionar...":
        print('t_cuenta')
        mensaje_error.exec_()
        return
    else:
        pass

    #Nombre de cuenta: No debe estar vacio
    nombre_cuenta = instancia_crear_cuenta.n_cuenta.text()
    if nombre_cuenta == "":
        print('nombre')
        mensaje_error.exec_()
        return
    
    else:
        pass

    #Saldo de cuenta: No debe estar vacio
    saldo_cuenta = instancia_crear_cuenta.s_cuenta.text()
    try:
        saldo_cuenta_prev = float(instancia_crear_cuenta.s_cuenta.text())
        saldo_cuenta = f'{dic_div[divisa]} {saldo_cuenta_prev:,.2f}'

    except:
        print('saldo')
        mensaje_error.exec_()
        return
        
    #No debemos llegar aquí si todas las variables no son correctas


    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO info_cartillas (divisa, t_cuenta, nombre, saldo) VALUES (?,?,?,?)""", (divisa, tipo_cuenta, nombre_cuenta, float(saldo_cuenta_prev)))

    conn.commit()
    conn.close()

    cartilla = cp.Cartilla(nombre_cuenta,saldo_cuenta)
    instancia_home.z_c_cuentas_ly.addWidget(cartilla.contenedor)
    instancia_crear_cuenta.close()



