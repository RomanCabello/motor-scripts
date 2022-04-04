import imp
from SQLManager import SqlManager
from FileManager import FileManager


direccion_servidor = ""
nombre_bd = ""
usuario = ""
password = ""

sql = SqlManager()
sql.obtener_conexion_sql_server(direccion_servidor, nombre_bd)

files = FileManager()
files.execute_scripts(1)
files.execute_scripts(2)