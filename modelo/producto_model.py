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
