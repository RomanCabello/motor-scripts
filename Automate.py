import pandas as pd
import pyodbc
from openpyxl import Workbook
from os import listdir


def obtener_conexion_sql_server():
    '''
    Este método genera una conexión a SQL server
    mediante una cadena con formato:
        DRIVER={ODBC Driver 17 for SQL Server};SERVER=<host>;DATABASE=<nombre_base>;UID=<usuario>;PWD=<password>
    '''
    #Parámetros para conexión
    direccion_servidor = "localhost"
    nombre_bd = "MisPruebas"
    nombre_usuario = "RomanCB"
    password = "RomanCB"
    sql_server_conn_str_ultra = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + direccion_servidor+';DATABASE='+nombre_bd+';Trusted_Connection=yes;'

    try:
        print("       [INFO] Intentando conectar a SQL server . . .")
        sql_server_conexion = pyodbc.connect(sql_server_conn_str_ultra)
        print("              . . . Conexión exitosa a SQL server.\n")
        return sql_server_conexion
    except Exception as e:
        print("       [ERROR] Ocurrió un error al conectar a SQL Server:", e,"\n")

def ejecutar_query(conexion,query):
    '''Este método permite ejecutar comandos de sql 
    con una conexion activa que se envía en los parámetros'''
    try:
        with conexion.cursor() as cursor:
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            data_o = cursor.fetchall()
            #print(data_o)
            data = [[value for value in row] for row in data_o]
            #print(data)
            df = pd.DataFrame(data, columns = columns)
        # print("       [INFO] La instrucción de SQL se ejecutó correctamente.")
        return df
    except Exception as e:
        print("\n       [ERROR] Ocurrió un error al buscar los valores: \n",  e,"\n")
        return pd.DataFrame()

my_files =  []
files = listdir("C:/Users/RomanCB/Documents/tests/")

with pd.ExcelWriter("Test.xlsx") as writer:  
    for file in files:
        name = ("C:/Users/RomanCB/Documents/tests/" + file)
        script = open(name, "r")
        conexion = obtener_conexion_sql_server()
        comandos = script.read()

        nombre_excel = file.rstrip(".sql")

        print (comandos)
        df = ejecutar_query(conexion, comandos)
        df.to_excel(writer, sheet_name=nombre_excel)
