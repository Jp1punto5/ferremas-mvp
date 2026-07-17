import sqlite3
import tempfile
import os


def setup_in_memory_db():
    """Crea una base de datos SQLite en archivo temporal (persistente entre conexiones)

    Retorna la ruta al archivo de la base de datos. Las pruebas deben parchear
    modelo.conexion.conectar para devolver nuevas conexiones a ese archivo.
    """
    fd, path = tempfile.mkstemp(prefix='test_ferremas_', suffix='.db')
    os.close(fd)

    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Crear tablas necesarias según los modelos
    cur.executescript('''
    CREATE TABLE categorias (
        id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    );

    CREATE TABLE productos (
        codigo_producto TEXT PRIMARY KEY,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio_cl REAL,
        precio_usd REAL,
        stock INTEGER,
        url_foto TEXT,
        id_categoria INTEGER,
        FOREIGN KEY(id_categoria) REFERENCES categorias(id_categoria)
    );

    CREATE TABLE usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_completo TEXT NOT NULL,
        correo TEXT NOT NULL UNIQUE,
        telefono TEXT,
        password_hash TEXT,
        rol TEXT
    );
    ''')

    # Insertar datos de ejemplo
    cur.execute("INSERT INTO categorias (nombre) VALUES (?)", ("Herramientas",))
    id_categoria = cur.lastrowid

    cur.execute(
        """INSERT INTO productos (codigo_producto, nombre, descripcion, precio_cl, precio_usd, stock, url_foto, id_categoria)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            'HER001',
            'Martillo carpintero',
            'Martillo de 16oz para carpintería',
            12000.0,
            12.8,
            10,
            '/vista/img/martillo.jpg',
            id_categoria
        )
    )

    # Usuario de prueba (password almacenado en claro igual que el código original espera)
    cur.execute(
        """INSERT INTO usuarios (nombre_completo, correo, telefono, password_hash, rol)
        VALUES (?, ?, ?, ?, ?)""",
        (
            'Juan Prueba',
            'juan@ejemplo.com',
            '+56912345678',
            'secret',
            'CLIENTE'
        )
    )

    conn.commit()
    conn.close()
    return path
