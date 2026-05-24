from modelo.conexion import ejecutar_consulta


# =========================
# LISTAR PRODUCTOS
# =========================

def obtener_productos():
    """
    Obtiene todos los productos de la BD con sus categorías.
    
    Returns:
        list: Lista de productos o lista vacía si hay error
    """
    try:
        query = """
            SELECT
                p.codigo_producto,
                p.nombre,
                p.descripcion,
                p.precio_cl,
                p.precio_usd,
                p.stock,
                p.url_foto,       
                c.nombre AS categoria
            FROM productos p
            INNER JOIN categorias c
                ON p.id_categoria = c.id_categoria
        """
        return ejecutar_consulta(query, fetch_one=False)
    except Exception as e:
        print(f"Error en obtener_productos: {e}")
        return []


# =========================
# OBTENER PRODUCTO
# =========================

def obtener_producto(codigo_producto):
    """
    Obtiene un producto específico por código.
    
    Args:
        codigo_producto (str): Código del producto
        
    Returns:
        sqlite3.Row: Producto encontrado o None
    """
    try:
        query = """
            SELECT
                p.codigo_producto,
                p.nombre,
                p.descripcion,
                p.precio_cl,
                p.precio_usd,
                p.stock,
                p.url_foto,
                c.nombre AS categoria
            FROM productos p
            INNER JOIN categorias c
                ON p.id_categoria = c.id_categoria
            WHERE p.codigo_producto = ?
        """
        return ejecutar_consulta(query, (codigo_producto,), fetch_one=True)
    except Exception as e:
        print(f"Error en obtener_producto: {e}")
        return None


# =========================
# OBTENER PRODUCTOS POR CATEGORIA
# =========================

def listar_productos_categoria(categoria):
    """
    Obtiene todos los productos de una categoría específica.
    
    Args:
        categoria (str): Nombre de la categoría
        
    Returns:
        list: Lista de productos de la categoría o lista vacía si hay error
    """
    try:
        query = """
            SELECT
                p.codigo_producto,
                p.nombre,
                p.descripcion,
                p.precio_cl,
                p.precio_usd,
                p.stock,
                p.url_foto,
                c.nombre AS categoria
            FROM productos p
            INNER JOIN categorias c
                ON p.id_categoria = c.id_categoria
            WHERE c.nombre = ?
        """
        return ejecutar_consulta(query, (categoria,), fetch_one=False)
    except Exception as e:
        print(f"Error en listar_productos_categoria: {e}")
        return []


# =========================
# ACTUALIZAR PRECIO USD
# =========================

def actualizar_precio_usd(codigo_producto, tasa_cambio):
    """
    Actualiza el precio en USD de un producto basado en precio_CL y tasa de cambio.
    
    Args:
        codigo_producto (str): Código del producto
        tasa_cambio (float): Tasa de cambio CLP a USD
        
    Returns:
        bool: True si se actualizó correctamente, False si hay error
    """
    try:
        query = """
            UPDATE productos
            SET precio_usd = ROUND(precio_cl / ?, 2)
            WHERE codigo_producto = ?
        """
        ejecutar_consulta(query, (tasa_cambio, codigo_producto), fetch_one=False)
        return True
    except Exception as e:
        print(f"Error en actualizar_precio_usd: {e}")
        return False


def actualizar_todos_precios_usd(tasa_cambio):
    """
    Actualiza los precios en USD de todos los productos.
    
    Args:
        tasa_cambio (float): Tasa de cambio CLP a USD
        
    Returns:
        dict: {"success": bool, "mensaje": str, "productos_actualizados": int}
    """
    try:
        query = """
            UPDATE productos
            SET precio_usd = ROUND(precio_cl / ?, 2)
        """
        ejecutar_consulta(query, (tasa_cambio,), fetch_one=False)
        
        query_count = "SELECT COUNT(*) as total FROM productos"
        resultado = ejecutar_consulta(query_count, fetch_one=True)
        productos_actualizados = resultado['total'] if resultado else 0
        
        return {
            "success": True,
            "mensaje": f"Precios USD actualizados correctamente",
            "productos_actualizados": productos_actualizados,
            "tasa_cambio_usada": tasa_cambio
        }
    except Exception as e:
        print(f"Error en actualizar_todos_precios_usd: {e}")
        return {
            "success": False,
            "mensaje": f"Error al actualizar precios: {str(e)}",
            "productos_actualizados": 0
        }
