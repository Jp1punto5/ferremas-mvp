import sqlite3

DATABASE = 'ferremas.db'


def conectar():
    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row
    return conexion