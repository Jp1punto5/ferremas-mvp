"""
Utilidades para formatear y transformar datos entre BD y API
"""


def formato_producto(producto):
    """
    Transforma un producto de la BD al formato esperado por la API.
    
    Args:
        producto (sqlite3.Row): Fila de producto de la BD
        
    Returns:
        dict: Producto formateado para la API
    """
    return {
        "codigo_producto": producto["codigo_producto"],
        "nombre": producto["nombre"],
        "descripcion": producto["descripcion"],
        "precio_cl": producto["precio_cl"],
        "precio_usd": producto["precio_usd"],
        "stock": producto["stock"],
        "url_foto": producto["url_foto"],
        "categoria": producto["categoria"]
    }


def respuesta_error(mensaje, codigo=400):
    """
    Crea una respuesta estándar para errores.
    
    Args:
        mensaje (str): Mensaje de error
        codigo (int): Código HTTP
        
    Returns:
        tuple: (dict, int) Respuesta y código HTTP
    """
    return {"success": False, "error": mensaje}, codigo


def respuesta_exito(data=None, mensaje="Operación exitosa"):
    """
    Crea una respuesta estándar para operaciones exitosas.
    
    Args:
        data (dict): Datos a retornar (opcional)
        mensaje (str): Mensaje de éxito
        
    Returns:
        tuple: (dict, int) Respuesta y código HTTP
    """
    respuesta = {"success": True, "mensaje": mensaje}
    if data:
        respuesta["data"] = data
    return respuesta, 200
