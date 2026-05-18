from modelo.conexion import ejecutar_consulta


# =========================
# OBTENER USUARIO POR CORREO
# =========================

def obtener_usuario_por_correo(correo):
    """
    Verifica si un correo está registrado en la BD.
    Útil para evitar registros duplicados y validar login.
    
    Args:
        correo (str): Correo del usuario
        
    Returns:
        sqlite3.Row: Usuario encontrado o None
    """
    try:
        query = """
            SELECT *
            FROM usuarios
            WHERE correo = ?
        """
        return ejecutar_consulta(query, (correo,), fetch_one=True)
    except Exception as e:
        print(f"Error en obtener_usuario_por_correo: {e}")
        return None


# =========================
# VALIDAR LOGIN
# =========================

def validar_login(correo, password):
    """
    Valida las credenciales de un usuario.
    
    Args:
        correo (str): Correo del usuario
        password (str): Contraseña del usuario
        
    Returns:
        sqlite3.Row: Usuario si credenciales son válidas, None si no
    """
    try:
        query = """
            SELECT *
            FROM usuarios
            WHERE correo = ?
            AND password_hash = ?
        """
        return ejecutar_consulta(query, (correo, password), fetch_one=True)
    except Exception as e:
        print(f"Error en validar_login: {e}")
        return None


# =========================
# REGISTRAR USUARIO
# =========================

def registrar_usuario(
        nombre_completo,
        correo,
        telefono,
        password
):
    """
    Registra un nuevo usuario en la BD.
    Por defecto todos los usuarios registrados son clientes.
    
    Args:
        nombre_completo (str): Nombre completo del usuario
        correo (str): Correo del usuario
        telefono (str): Teléfono del usuario
        password (str): Contraseña del usuario
        
    Raises:
        Exception: Si hay error en la BD
    """
    try:
        query = """
            INSERT INTO usuarios
            (
                nombre_completo,
                correo,
                telefono,
                password_hash,
                rol
            )
            VALUES (?, ?, ?, ?, ?)
        """
        conexion = None
        from modelo.conexion import conectar
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute(query, (
                nombre_completo,
                correo,
                telefono,
                password,
                'CLIENTE'
            ))
            conexion.commit()
        finally:
            if conexion:
                conexion.close()
    except Exception as e:
        print(f"Error en registrar_usuario: {e}")
        raise
