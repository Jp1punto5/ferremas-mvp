from modelo.conexion import conectar


# =========================
# OBTENER USUARIO POR CORREO

# la finalidad de esta función es verificar si un correo ya está registrado en la base de datos,
#  lo cual es útil para evitar registros duplicados y para validar el proceso de login.
# =========================

def obtener_usuario_por_correo(correo):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM usuarios
        WHERE correo = ?
    """, (correo,))

    usuario = cursor.fetchone()

    conexion.close()

    return usuario


# =========================
# VALIDAR LOGIN
# =========================

def validar_login(correo, password):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM usuarios
        WHERE correo = ?
        AND password_hash = ?
    """, (correo, password))

    usuario = cursor.fetchone()

    conexion.close()

    return usuario


# =========================
# REGISTRAR USUARIO
# =========================

def registrar_usuario(
        nombre_completo,
        correo,
        telefono,
        password
):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO usuarios
        (
            nombre_completo,
            correo,
            telefono,
            password_hash,
            rol
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        nombre_completo,
        correo,
        telefono,
        password,
        'CLIENTE' #De momento por defecto todos los usuarios registrados serán clientes
    ))

    conexion.commit()

    conexion.close()