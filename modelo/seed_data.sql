/* ========================================= */
/* LIMPIAR TABLAS */
/* ========================================= */

DELETE FROM productos;
DELETE FROM categorias;
DELETE FROM usuarios;


/* ========================================= */
/* RESETEAR AUTOINCREMENT */
/* ========================================= */

DELETE FROM sqlite_sequence;


/* ========================================= */
/* INSERTAR USUARIOS */
/* ========================================= */

INSERT INTO usuarios (
    nombre_completo,
    correo,
    telefono,
    password_hash,
    rol
)
VALUES
(
    'Juan Cliente',
    'cliente@ferremas.cl',
    '+56911111111',
    '123456',
    'CLIENTE'
),
(
    'Admin Ferremas',
    'admin@ferremas.cl',
    '+56922222222',
    'admin123',
    'ADMIN'
);


/* ========================================= */
/* INSERTAR CATEGORIAS */
/* ========================================= */

INSERT INTO categorias (nombre)
VALUES
('Herramientas'),
('Electricidad'),
('Construcción'),
('Pintura'),
('Jardinería'),
('Seguridad');

/* ========================================= */
/* INSERTAR PRODUCTOS */
/* ========================================= */

INSERT INTO productos (
    codigo_producto,
    nombre,
    descripcion,
    precio,
    stock,
    url_foto,
    id_categoria
)
VALUES

/* ========================================= */
/* HERRAMIENTAS */
/* ========================================= */

(
    'HER001',
    'Martillo carpintero',
    'Martillo profesional acero reforzado',
    7990,
    15,
    'css/herramientas/martillo.png',
    1
),

(
    'HER002',
    'Taladro inalámbrico',
    'Taladro 20V batería incluida',
    89990,
    8,
    'css/herramientas/taladro.png',
    1
),

(
    'HER003',
    'Caja herramientas',
    'Caja metálica profesional',
    24990,
    10,
    'css/herramientas/caja_herramientas.png',
    1
),

/* ========================================= */
/* ELECTRICIDAD */
/* ========================================= */

(
    'ELE001',
    'Cable eléctrico',
    'Cable 100 metros',
    15990,
    25,
    'css/herramientas/cable_electrico.png',
    2
),

(
    'ELE002',
    'Enchufe doble',
    'Enchufe doble blanco',
    3990,
    40,
    'css/herramientas/enchufe_doble.png',
    2
),

(
    'ELE003',
    'Interruptor',
    'Interruptor simple',
    2990,
    35,
    'css/herramientas/interruptor.png',
    2
),

/* ========================================= */
/* CONSTRUCCION */
/* ========================================= */

(
    'CON001',
    'Saco cemento',
    'Cemento alta resistencia',
    5990,
    50,
    'css/herramientas/saco_cemento.png',
    3
),

(
    'CON002',
    'Ladrillo fiscal',
    'Ladrillo cerámico',
    790,
    500,
    'css/herramientas/ladrillo.png',
    3
),

(
    'CON003',
    'Pala construcción',
    'Pala metálica reforzada',
    12990,
    20,
    'css/herramientas/pala_construccion.png',
    3
),

/* ========================================= */
/* PINTURA */
/* ========================================= */

(
    'PIN001',
    'Rodillo pintura',
    'Rodillo profesional',
    4990,
    30,
    'css/herramientas/rodillo_pintura.png',
    4
),

(
    'PIN002',
    'Pintura blanca',
    'Galón pintura interior',
    19990,
    18,
    'css/herramientas/pintura_blanca.png',
    4
),

(
    'PIN003',
    'Brocha profesional',
    'Brocha madera natural',
    2990,
    45,
    'css/herramientas/brocha.png',
    4
),

/* ========================================= */
/* JARDINERIA */
/* ========================================= */

(
    'JAR001',
    'Manguera jardín',
    'Manguera flexible 20 metros',
    14990,
    12,
    'css/herramientas/manguera.png',
    5
),

(
    'JAR002',
    'Tijera poda',
    'Tijera acero inoxidable',
    8990,
    16,
    'css/herramientas/tijera_poda.png',
    5
),

(
    'JAR003',
    'Macetero grande',
    'Macetero cerámico',
    6990,
    22,
    'css/herramientas/macetero_grande.png',
    5
),

/* ========================================= */
/* SEGURIDAD */
/* ========================================= */

(
    'SEG001',
    'Casco seguridad',
    'Casco industrial amarillo',
    12990,
    14,
    'css/herramientas/casco_seguridad.png',
    6
),

(
    'SEG002',
    'Guantes trabajo',
    'Guantes anticorte',
    5990,
    28,
    'css/herramientas/guantes.png',
    6
),

(
    'SEG003',
    'Lentes protección',
    'Lentes transparentes',
    4990,
    25,
    'css/herramientas/lentes_proteccion.png',
    6
);