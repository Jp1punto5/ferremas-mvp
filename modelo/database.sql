

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_completo TEXT NOT NULL,
    correo TEXT UNIQUE NOT NULL,
    telefono TEXT,
    password_hash TEXT NOT NULL,
    rol TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS productos (

    codigo_producto TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    precio_CL REAL NOT NULL DEFAULT 0,
    precio_USD REAL NOT NULL DEFAULT 0,
    stock INTEGER NOT NULL DEFAULT 0,
    url_foto TEXT,
    id_categoria INTEGER,
    FOREIGN KEY (id_categoria)
    REFERENCES categorias(id_categoria)
);