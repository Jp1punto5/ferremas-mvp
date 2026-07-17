# SHIM: La lógica real de la base de datos ahora se gestiona en ferremas-api (modelo/conexion.py).
# Este archivo expone la misma interfaz (conectar, ejecutar_consulta) pero por defecto
# lanza un error informativo para recordar que la BD real debe consultarse vía ferremas-api.
# Tests unitarios pueden parchear modelo.conexion.conectar para usar una DB temporal.

import logging
import os

logger = logging.getLogger(__name__)


def conectar():
    """
    Placeholder conectar() en ferremas-mvp. No conecta a la BD local. Tests pueden parchear esta
    función para proporcionar una conexión a un archivo SQLite temporal.

    Raises:
        RuntimeError: Indica que la lógica real quedó en ferremas-api
    """
    raise RuntimeError(
        "La lógica de la base de datos real fue movida a ferremas-api.\n"
        "Para ejecutar acciones sobre la BD en producción, use ferremas-api.\n"
        "En pruebas, parchea modelo.conexion.conectar para devolver una conexión SQLite temporal."
    )


def ejecutar_consulta(query, params=None, fetch_one=False):
    """
    Ejecuta una consulta usando la función conectar().
    - En ejecución normal `conectar()` lanza RuntimeError (la BD real está en ferremas-api).
    - En tests, `modelo.conexion.conectar` debe ser parcheada para devolver una conexión sqlite3 a un archivo temporal.

    Args:
        query (str): SQL a ejecutar
        params (tuple|list|None): parámetros para la consulta
        fetch_one (bool): si True devuelve un solo registro como dict; si False devuelve lista de dicts o None para DML

    Returns:
        dict|list|None
    """
    conn = conectar()  # En tests se parchea para devolver conexión válida
    cursor = conn.cursor()
    params = params or ()
    cursor.execute(query, params)

    if query.strip().lower().startswith('select'):
        rows = cursor.fetchall()
        # Si no hay descripción, devolver lista vacía
        if not cursor.description:
            return []
        cols = [d[0] for d in cursor.description]
        if fetch_one:
            if not rows:
                return None
            return dict(zip(cols, rows[0]))
        else:
            return [dict(zip(cols, r)) for r in rows]
    else:
        # INSERT/UPDATE/DELETE
        conn.commit()
        return None
