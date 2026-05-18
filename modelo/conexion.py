import sqlite3
import logging

DATABASE = 'ferremas.db'
logger = logging.getLogger(__name__)


def conectar():
    """
    Establece conexión con la base de datos SQLite.
    
    Returns:
        sqlite3.Connection: Conexión a la BD
        
    Raises:
        Exception: Si hay error en la conexión
    """
    try:
        conexion = sqlite3.connect(DATABASE)
        conexion.row_factory = sqlite3.Row
        return conexion
    except sqlite3.Error as e:
        logger.error(f"Error conectando a BD: {e}")
        raise Exception(f"No se pudo conectar a la base de datos: {str(e)}")


def ejecutar_consulta(query, params=None, fetch_one=False):
    """
    Ejecuta una consulta SQL y retorna resultados de forma segura.
    
    Args:
        query (str): Consulta SQL
        params (tuple): Parámetros para prevenir SQL injection
        fetch_one (bool): Si True, retorna un registro; si False, retorna todos
        
    Returns:
        Row o list: Resultado(s) de la consulta
        
    Raises:
        Exception: Si hay error en la BD
    """
    conexion = None
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch_one:
            resultado = cursor.fetchone()
        else:
            resultado = cursor.fetchall()
        
        conexion.commit()
        return resultado
    
    except sqlite3.Error as e:
        logger.error(f"Error ejecutando consulta: {e}")
        raise Exception(f"Error en la base de datos: {str(e)}")
    finally:
        if conexion:
            conexion.close()