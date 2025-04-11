from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
import complementos as cp
import locale
import sqlite3 as sql
import datetime
import os

locale.setlocale(locale.LC_NUMERIC, 'es_ES.UTF-8')
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_bbdd = os.path.join(ruta_base, "recursos", "bbdd_general.db")
#Diccionario para divisas
dic_div = {'PEN':"S/.", 'USD':'USD'}


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
    fecha DATE,
    ciclo_facturacion TEXT,
    fecha_pago DATE)
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS log_acciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_accion DATE,
    evento TEXT)
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS m_proyectados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    t_transaccion TEXT,
    monto TEXT,
    cuenta_prin TEXT,
    cuenta_det TEXT,
    categoria TEXT,
    nota TEXT,
    fecha DATE,
    ciclo_facturacion TEXT,
    fecha_pago DATE)
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
    

    mensaje_error = QMessageBox(parent=instancia_crear_cuenta)
    mensaje_error.setIcon(QMessageBox.Critical)
    mensaje_error.setText('Revisa los campos')
    mensaje_error.setWindowTitle("Atención")

    #Definición de variables
    #Divisa: No debe ser Seleccionar...
    divisa = instancia_crear_cuenta.divisas.currentText()
    if divisa == "Seleccionar...":
        mensaje_error.exec_()
        return
    else:
        pass

    #Tipo de cuenta: No debe ser Seleccionar...
    tipo_cuenta = instancia_crear_cuenta.tipo.currentText()
    if tipo_cuenta == "Seleccionar...":
        mensaje_error.exec_()
        return
    else:
        pass

    #Nombre de cuenta: No debe estar vacio
    nombre_cuenta = instancia_crear_cuenta.n_cuenta.text()
    if nombre_cuenta == "":
        mensaje_error.exec_()
        return
    
    else:
        pass

    #Saldo de cuenta: No debe estar vacio
    saldo_cuenta = instancia_crear_cuenta.s_cuenta.text()
    try:
        saldo_cuenta_prev = float(saldo_cuenta)

    except:
        mensaje_error.exec_()
        return
        
    #No debemos llegar aquí si todas las variables no son correctas

    elementos = ["Ingreso",saldo_cuenta_prev,nombre_cuenta,None,"Saldo Inicial","Creación de cuenta",str(datetime.date.today()),None,None]
 
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO transacciones (t_transaccion, monto, cuenta_prin, cuenta_det, categoria, nota, fecha, ciclo_facturacion, fecha_pago) VALUES(?,?,?,?,?,?,?,?,?)", elementos)
    saldo_cuenta_real = cursor.execute("SELECT SUM(monto) FROM transacciones").fetchone()[0]
    cursor.execute("""INSERT INTO info_cartillas (divisa, t_cuenta, nombre, saldo) VALUES (?,?,?,?)""", (divisa, tipo_cuenta, nombre_cuenta, float(saldo_cuenta_real)))
    
    
    conn.commit()
    conn.close()

    actualizar_tabla_registros(instancia_home)
    cartilla = cp.Cartilla(nombre_cuenta,f'{dic_div[divisa]} {str(saldo_cuenta_real)}')
    instancia_home.z_c_cuentas_ly.addWidget(cartilla.contenedor)
    instancia_crear_cuenta.close()

def cargar_saldos(instancia_home):
    conn = conectar_bd()
    cursor = conn.cursor()

    cuentas = cursor.execute("SELECT DISTINCT nombre FROM info_cartillas")
    cuentas = cuentas.fetchall()

    for tupla in cuentas:
        nombre = tupla[0]
        ingresos_cuenta = cursor.execute('SELECT SUM(monto) FROM transacciones WHERE cuenta_prin = ? AND t_transaccion = ?',(nombre,"Ingreso"))
        try:
            sum_ingresos = float(ingresos_cuenta.fetchone()[0])
        except:
            sum_ingresos=0

        egresos_cuenta = cursor.execute('SELECT SUM(monto) FROM transacciones WHERE cuenta_prin = ? AND t_transaccion = ?',(nombre,"Gasto"))
        try:
            sum_egresos = float(egresos_cuenta.fetchone()[0])
        except:
            sum_egresos = 0

        saldo = float(sum_ingresos-sum_egresos)

        divisa = cursor.execute('SELECT divisa FROM info_cartillas WHERE nombre = ?',(nombre,))
        divisa = divisa.fetchone()[0]

        cursor.execute("UPDATE info_cartillas SET saldo = ? WHERE nombre = ?", (saldo, nombre))

        cartilla = cp.Cartilla(nombre, f'{dic_div[divisa]} {str(saldo)}')
        instancia_home.z_c_cuentas_ly.addWidget(cartilla.contenedor)


    conn.close()

def nuevo_registro(instancia_relativa):
    ventana_nr = cp.CreacionRegistro(parent= instancia_relativa)
    ventana_nr.show()

def nuevo_registro_proyect(instancia_relativa):
    ventana_nr = cp.CreacionRegistroProyect(parent= instancia_relativa)
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
    instancia_home.registros.setHorizontalHeaderLabels(['Id','Tipo_transacción','Monto','Cuenta', 'Cuenta Destino', 'Categoria', 'Nota', 'Fecha','Ciclo Facturación', 'Fecha a pagar'])

    for i, registro in enumerate(registros):
        for j, campo in enumerate(registro):
            item = QTableWidgetItem(str(campo))
            instancia_home.registros.setItem(i,j,item)

def actualizar_tabla_proyect (instancia_proyec):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM m_proyectados')
    registros = cursor.fetchall()
    conn.close()

    if not registros:
        instancia_proyec.tabla_proyectados.setRowCount(0)
        instancia_proyec.tabla_proyectados.setColumnCount(0)

        return

    instancia_proyec.tabla_proyectados.setRowCount(len(registros))
    instancia_proyec.tabla_proyectados.setColumnCount(len(registros[0]))
    instancia_proyec.tabla_proyectados.setHorizontalHeaderLabels(['Id','Tipo_transacción','Monto','Cuenta', 'Cuenta Destino', 'Categoria', 'Nota', 'Fecha','Ciclo Facturación', 'Fecha a pagar'])

    for i, registro in enumerate(registros):
        for j, campo in enumerate(registro):
            item = QTableWidgetItem(str(campo))
            instancia_proyec.tabla_proyectados.setItem(i,j,item)

def crear_registro(instancia_home,instancia_creacion_registro):

    conn = conectar_bd()
    cursor = conn.cursor()

    #CALCULO FECHA DE PAGO Y PERIODO DE FACTURACIÓN
    t_cuenta = cursor.execute("SELECT t_cuenta FROM info_cartillas WHERE nombre = ? ",(instancia_creacion_registro.cuenta_invo.currentText(),))
    t_cuenta = t_cuenta.fetchone()[0]

    fecha_temp = instancia_creacion_registro.fecha.date().toString("dd-MM-yyyy")
    fecha_temp=datetime.datetime.strptime(fecha_temp, "%d-%m-%Y")
    dia_fac = 4

    if t_cuenta == "Tarjeta de Crédito" and instancia_creacion_registro.t_transaccion.currentText() == "Gasto":
        if int(fecha_temp.day) < dia_fac+1 and int(fecha_temp.month) == 12:
            fecha_pagar = f'01/01/{int(fecha_temp.year)+1}'
            fecha_pagar = datetime.datetime.strptime(fecha_pagar, "%d/%m/%Y").date()
            if int(fecha_pagar.month) == 1:
                ciclo_facturacion = f'Ciclo 11-12'
            elif int(fecha_pagar.month) == 2:
                ciclo_facturacion = f'Ciclo 12-01'
            else:
                ciclo_facturacion = f'Ciclo {int(fecha_pagar.month)-2}-{int(fecha_pagar.month)-1}'
        
        elif int(fecha_temp.day) >= dia_fac+1 and int(fecha_temp.month) == 11:
            fecha_pagar = f'01/01/{int(fecha_temp.year)+1}'
            fecha_pagar = datetime.datetime.strptime(fecha_pagar, "%d/%m/%Y").date()
            if int(fecha_pagar.month) == 1:
                ciclo_facturacion = f'Ciclo 11-12'
            elif int(fecha_pagar.month) == 2:
                ciclo_facturacion = f'Ciclo 12-01'
            else:
                ciclo_facturacion = f'Ciclo {int(fecha_pagar.month)-2}-{int(fecha_pagar.month)-1}'
        
        elif int(fecha_temp.day) < dia_fac+1:
            fecha_pagar = f'01/{int(fecha_temp.month)+1}/{fecha_temp.year}'
            fecha_pagar = datetime.datetime.strptime(fecha_pagar, "%d/%m/%Y").date()
            if int(fecha_pagar.month) == 1:
                ciclo_facturacion = f'Ciclo 11-12'
            elif int(fecha_pagar.month) == 2:
                ciclo_facturacion = f'Ciclo 12-01'
            else:
                ciclo_facturacion = f'Ciclo {int(fecha_pagar.month)-2}-{int(fecha_pagar.month)-1}'
        
        else:
            fecha_pagar = f'01/{int(fecha_temp.month)+2}/{fecha_temp.year}'
            fecha_pagar = datetime.datetime.strptime(fecha_pagar, "%d/%m/%Y").date()
            if int(fecha_pagar.month) == 1:
                ciclo_facturacion = f'Ciclo 11-12'
            elif int(fecha_pagar.month) == 2:
                ciclo_facturacion = f'Ciclo 12-01'
            else:
                ciclo_facturacion = f'Ciclo {int(fecha_pagar.month)-2}-{int(fecha_pagar.month)-1}'

    else:
        ciclo_facturacion = None
        fecha_pagar = None

    #PROCESO DE INSERTAR INFO DEL FORMULARIO A LA BBDD
    elementos = [instancia_creacion_registro.t_transaccion.currentText(),
                 instancia_creacion_registro.monto.text(), 
                 instancia_creacion_registro.cuenta_invo.currentText(),
                 instancia_creacion_registro.cuenta_dest.currentText(), 
                 instancia_creacion_registro.categorias.currentText(),
                 instancia_creacion_registro.nota.text(),
                 instancia_creacion_registro.fecha.date().toString("dd-MM-yyyy"),
                 ciclo_facturacion,
                 fecha_pagar]
    

    cursor.execute("INSERT INTO transacciones (t_transaccion, monto, cuenta_prin, cuenta_det, categoria, nota, fecha, ciclo_facturacion, fecha_pago) VALUES(?,?,?,?,?,?,?,?,?)", elementos)

    conn.commit()
    conn.close()

    actualizar_tabla_registros(instancia_home)
    limpiar_layout(instancia_home.z_c_cuentas_ly)
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
        
        for id_registro in ids_registros:
            cursor.execute("DELETE FROM transacciones WHERE id = ?", (id_registro,))

        conn.commit()

    actualizar_tabla_registros(instancia_home)
    limpiar_layout(instancia_home.z_c_cuentas_ly)
    cargar_saldos(instancia_home)
    conn.close()

def eliminar_registros_proyect(instancia_proyect):

    #PROCESO ELIMINACIÓN DE REGISTROS EN BBDD
    #Identifica qué filas están seleccionadas
    filas_selec = instancia_proyect.tabla_proyectados.selectionModel().selectedRows()

    #En caso no haya filas seleccionadas
    if not filas_selec:
        QMessageBox.warning(instancia_proyect,'Error', 'Selecciona al menos un registro para eliminar')
        return

    #Recupera todos los valores de la columna 0 (id) de las filas que hayan estado seleccionadas
    ids_registros = [instancia_proyect.tabla_proyectados.item(fila.row(),0).text() for fila in filas_selec]


    #Mensaje de confirmación de eliminación
    respuesta = QMessageBox.question(instancia_proyect, "Confirmación",
                                     f"¿Estás seguro de que deseas eliminar {len(ids_registros)} registros?",
                                     QMessageBox.Yes | QMessageBox.No)
    
    #Si se elige "Yes" en mensaje de confirmación
    if respuesta == QMessageBox.Yes:

        #Conectar con la base de datos
        conn = conectar_bd()
        cursor = conn.cursor()

        #Por cada id de la lista de ids_registros va a eliminarlos de la bbdd
        for id_registro in ids_registros:
            cursor.execute("DELETE FROM m_proyectados WHERE id = ?", (id_registro,))
            conn.commit()
        
        conn.close()

    elif respuesta == QMessageBox.No:
        return
    
    else:
        return

    actualizar_tabla_proyect(instancia_proyect)
   
def limpiar_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()

def ir_proyectado(instancia_stacked):
    instancia_stacked.setCurrentIndex(1)

def crear_registro_proyec(instancia_proyec,instancia_creacion_registro):

    conn = conectar_bd()
    cursor = conn.cursor()
    t_cuenta = cursor.execute("SELECT t_cuenta FROM info_cartillas WHERE nombre = ? ",(instancia_creacion_registro.cuenta_invo.currentText(),))
    t_cuenta = t_cuenta.fetchone()[0]
    print(t_cuenta)

    fecha_temp = instancia_creacion_registro.fecha.date().toString("dd-MM-yyyy")
    fecha_temp=datetime.datetime.strptime(fecha_temp, "%d-%m-%Y")
    dia_fac = 4

    if t_cuenta == "Tarjeta de Crédito" and instancia_creacion_registro.t_transaccion.currentText() == "Gasto":
        if int(fecha_temp.day) < dia_fac+1 and int(fecha_temp.month) == 12:
            fecha_pagar = f'01/01/{int(fecha_temp.year)+1}'
            fecha_pagar = datetime.datetime.strptime(fecha_pagar, "%d/%m/%Y").date()
            if int(fecha_pagar.month) == 1:
                ciclo_facturacion = f'Ciclo 11-12'
            elif int(fecha_pagar.month) == 2:
                ciclo_facturacion = f'Ciclo 12-01'
            else:
                ciclo_facturacion = f'Ciclo {int(fecha_pagar.month)-2}-{int(fecha_pagar.month)-1}'
        
        elif int(fecha_temp.day) >= dia_fac+1 and int(fecha_temp.month) == 11:
            fecha_pagar = f'01/01/{int(fecha_temp.year)+1}'
            fecha_pagar = datetime.datetime.strptime(fecha_pagar, "%d/%m/%Y").date()
            if int(fecha_pagar.month) == 1:
                ciclo_facturacion = f'Ciclo 11-12'
            elif int(fecha_pagar.month) == 2:
                ciclo_facturacion = f'Ciclo 12-01'
            else:
                ciclo_facturacion = f'Ciclo {int(fecha_pagar.month)-2}-{int(fecha_pagar.month)-1}'
        
        elif int(fecha_temp.day) < dia_fac+1:
            fecha_pagar = f'01/{int(fecha_temp.month)+1}/{fecha_temp.year}'
            fecha_pagar = datetime.datetime.strptime(fecha_pagar, "%d/%m/%Y").date()
            if int(fecha_pagar.month) == 1:
                ciclo_facturacion = f'Ciclo 11-12'
            elif int(fecha_pagar.month) == 2:
                ciclo_facturacion = f'Ciclo 12-01'
            else:
                ciclo_facturacion = f'Ciclo {int(fecha_pagar.month)-2}-{int(fecha_pagar.month)-1}'
        
        else:
            fecha_pagar = f'01/{int(fecha_temp.month)+2}/{fecha_temp.year}'
            fecha_pagar = datetime.datetime.strptime(fecha_pagar, "%d/%m/%Y").date()
            if int(fecha_pagar.month) == 1:
                ciclo_facturacion = f'Ciclo 11-12'
            elif int(fecha_pagar.month) == 2:
                ciclo_facturacion = f'Ciclo 12-01'
            else:
                ciclo_facturacion = f'Ciclo {int(fecha_pagar.month)-2}-{int(fecha_pagar.month)-1}'

    else:
        ciclo_facturacion = None
        fecha_pagar = None

    elementos = [instancia_creacion_registro.t_transaccion.currentText(),
                 instancia_creacion_registro.monto.text(), 
                 instancia_creacion_registro.cuenta_invo.currentText(),
                 instancia_creacion_registro.cuenta_dest.currentText(), 
                 instancia_creacion_registro.categorias.currentText(),
                 instancia_creacion_registro.nota.text(),
                 instancia_creacion_registro.fecha.date().toString("dd-MM-yyyy"),
                 ciclo_facturacion,
                 fecha_pagar]
    


    cursor.execute("INSERT INTO m_proyectados (t_transaccion, monto, cuenta_prin, cuenta_det, categoria, nota, fecha, ciclo_facturacion, fecha_pago) VALUES(?,?,?,?,?,?,?,?,?)", elementos)
    
    conn.commit()
    conn.close()

    actualizar_tabla_proyect(instancia_proyec)

    instancia_creacion_registro.close()

def cometer_registros(instancia_home, instancia_proyect):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO transacciones (
        t_transaccion, monto, cuenta_prin, cuenta_det, categoria, nota, fecha, ciclo_facturacion, fecha_pago
    )
    SELECT 
        t_transaccion, monto, cuenta_prin, cuenta_det, categoria, nota, fecha, ciclo_facturacion, fecha_pago 
    FROM m_proyectados
''')

    conn.commit()
    conn.close()

    actualizar_tabla_proyect(instancia_proyect)
    actualizar_tabla_registros(instancia_home)
    limpiar_layout(instancia_home.z_c_cuentas_ly)
    cargar_saldos(instancia_home)


