from modelo.conexion import conectar


# =========================
# LISTAR PRODUCTOS
# =========================

def obtener_productos():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            p.codigo_producto,
            p.nombre,
            p.descripcion,
            p.precio,
            p.stock,
            p.url_foto,       
            c.nombre AS categoria
        FROM productos p
        INNER JOIN categorias c
            ON p.id_categoria = c.id_categoria
    """)

    productos = cursor.fetchall()

    conexion.close()

    return productos


# =========================
# OBTENER PRODUCTO
# =========================

def obtener_producto(codigo_producto):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            p.codigo_producto,
            p.nombre,
            p.descripcion,
            p.precio,
            p.stock,
            c.nombre AS categoria
        FROM productos p
        INNER JOIN categorias c
            ON p.id_categoria = c.id_categoria
        WHERE p.codigo_producto = ?
    """, (codigo_producto,))

    producto = cursor.fetchone()

    conexion.close()

    return producto