from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
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
    saldo FLOAT)
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transacciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    t_transaccion TEXT,
    monto TEXT,
    cuenta_prin TEXT,
    cuenta_det TEXT,
    categoria TEXT,
    nota TEXT,
    fecha DATE)
    ''')
    
    conexion.commit()
    conexion.close()

crear_bbdd()

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


    try:
        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("""INSERT INTO info_cartillas (divisa, t_cuenta, nombre, saldo) VALUES (?,?,?,?)""", (divisa, tipo_cuenta, nombre_cuenta, float(saldo_cuenta_prev)))

        conn.commit()
        conn.close()

        cartilla = cp.Cartilla(nombre_cuenta,saldo_cuenta)
        instancia_home.z_c_cuentas_ly.addWidget(cartilla.contenedor)
        instancia_crear_cuenta.close()

    except:
        mensaje_error.exec()

def cargar_saldos(instancia_home):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("SELECT nombre, saldo FROM info_cartillas")
    saldos = cursor.fetchall()

    for nombre, saldo in saldos:
        saldo_format = f'{saldo:,.2f}'

        cartilla = cp.Cartilla(nombre,saldo_format)

        instancia_home.z_c_cuentas_ly.addWidget(cartilla.contenedor)
    
    conn.close()

def nuevo_registro(instancia_home):
    ventana_nr = cp.CreacionRegistro(parent= instancia_home)
    ventana_nr.show()

def traer_nombres():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(''' SELECT nombre FROM info_cartillas''')
    nombres = cursor.fetchall()

    conn.close()

    lista_nombres = []

    for i in nombres:
        lista_nombres.append(i[0])

    return lista_nombres

def actualizar_tabla_registros (instancia_home):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM transacciones')
    registros = cursor.fetchall()
    conn.close()

    if not registros:
        instancia_home.registros.setRowCount(0)
        instancia_home.registros.setColumnCount(0)

        return

    instancia_home.registros.setRowCount(len(registros))
    instancia_home.registros.setColumnCount(len(registros[0]))
    instancia_home.registros.setHorizontalHeaderLabels(['Id','Tipo_transacción','Monto','Cuenta', 'Cuenta Destino', 'Categoria', 'Nota', 'Fecha'])

    for i, registro in enumerate(registros):
        for j, campo in enumerate(registro):
            item = QTableWidgetItem(str(campo))
            instancia_home.registros.setItem(i,j,item)

def crear_registro(instancia_home,instancia_creacion_registro):
    elementos = [instancia_creacion_registro.t_transaccion.currentText(),
                 instancia_creacion_registro.monto.text(), 
                 instancia_creacion_registro.cuenta_invo.currentText(),
                 instancia_creacion_registro.cuenta_dest.currentText(), 
                 instancia_creacion_registro.categorias.currentText(),
                 instancia_creacion_registro.nota.text(),
                 instancia_creacion_registro.fecha.date().toString("dd-MM-yyyy")]
    
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO transacciones (t_transaccion, monto, cuenta_prin, cuenta_det, categoria, nota, fecha) VALUES(?,?,?,?,?,?,?)", elementos)
    cursor.execute("SELECT saldo FROM info_cartillas WHERE nombre = ? ",(instancia_creacion_registro.cuenta_invo.currentText(),))
    saldo = float(cursor.fetchone()[0])
    monto = float(instancia_creacion_registro.monto.text())
    
    if instancia_creacion_registro.t_transaccion.currentText() == "Ingreso":
        actualizador = saldo + monto
        cursor.execute("UPDATE info_cartillas SET saldo = ? WHERE nombre = ?", (actualizador,instancia_creacion_registro.cuenta_invo.currentText()))
        limpiar_layout(instancia_home.z_c_cuentas_ly)

        print(actualizador)
    
    elif instancia_creacion_registro.t_transaccion.currentText() == "Gasto":
        actualizador = saldo - monto
        cursor.execute("UPDATE info_cartillas SET saldo = ? WHERE nombre = ?", (actualizador,instancia_creacion_registro.cuenta_invo.currentText()))
        limpiar_layout(instancia_home.z_c_cuentas_ly)
        print(actualizador)
    
    else:
        print('transferencia')


    conn.commit()
    conn.close()

    actualizar_tabla_registros(instancia_home)
    cargar_saldos(instancia_home)

    instancia_creacion_registro.close()

def eliminar_registros(instancia_home):

    #PROCESO ELIMINACIÓN DE REGISTROS EN BBDD
    #Identifica qué filas están seleccionadas
    filas_selec = instancia_home.registros.selectionModel().selectedRows()

    #En caso no haya filas seleccionadas
    if not filas_selec:
        QMessageBox.warning(instancia_home,'Error', 'Selecciona al menos un registro para eliminar')
        return

    #Recupera todos los valores de la columna 0 (id) de las filas que hayan estado seleccionadas
    ids_registros = [instancia_home.registros.item(fila.row(),0).text() for fila in filas_selec]


    #Mensaje de confirmación de eliminación
    respuesta = QMessageBox.question(instancia_home, "Confirmación",
                                     f"¿Estás seguro de que deseas eliminar {len(ids_registros)} registros?",
                                     QMessageBox.Yes | QMessageBox.No)
    
    #Si se elige "Yes" en mensaje de confirmación
    if respuesta == QMessageBox.Yes:
        #Conectar con la base de datos
        conn = sql.connect(rf'{ruta_bbdd}')
        cursor = conn.cursor()

        #Por cada id de la lista de ids_registros va a eliminarlos de la bbdd
        for id_registro in ids_registros:
            cursor.execute("SELECT cuenta_prin FROM transacciones WHERE id = ?",(id_registro,))
            nombre_cuenta = cursor.fetchone()[0]

            cursor.execute("SELECT t_transaccion FROM transacciones WHERE id = ?",(id_registro,))
            tipo_transaccion = cursor.fetchone()[0]

            cursor.execute("SELECT monto FROM transacciones WHERE id = ?",(id_registro,))
            monto = float(cursor.fetchone()[0])

            cursor.execute("SELECT saldo FROM info_cartillas WHERE nombre = ?",(nombre_cuenta,))
            saldo_actual_cuenta = cursor.fetchone()[0]

            if tipo_transaccion == "Ingreso":
                actualizador = saldo_actual_cuenta - monto
                cursor.execute("UPDATE info_cartillas SET saldo = ? WHERE nombre = ?", (actualizador,nombre_cuenta))

            elif tipo_transaccion == "Gasto":
                actualizador = saldo_actual_cuenta+monto
                cursor.execute("UPDATE info_cartillas SET saldo = ? WHERE nombre = ?", (actualizador,nombre_cuenta))

            else:
                print('transferencia')
            
            cursor.execute("DELETE FROM transacciones WHERE id = ?", (id_registro,))

            conn.commit()

    actualizar_tabla_registros(instancia_home)
    limpiar_layout(instancia_home.z_c_cuentas_ly)
    cargar_saldos(instancia_home)
    conn.close()

def limpiar_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()
