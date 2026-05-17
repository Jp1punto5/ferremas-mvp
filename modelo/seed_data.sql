-- Limpiamos las tablas para evitar duplicados
DELETE FROM productos;
DELETE FROM categorias;
DELETE FROM usuarios;


--Categorías DEMO
INSERT INTO categorias (nombre) VALUES
('Herramientas'),
('Tornillería'),
('Pinturas'),
('Electricidad'),
('Gasfitería'),
('Seguridad');


--Herramientas
INSERT INTO productos
(codigo_producto, nombre, descripcion, precio, stock, id_categoria)
VALUES
('HER001', 'Martillo', 'Martillo de acero 16oz', 7990, 25, 1),

('HER002', 'Destornillador Phillips', 'Destornillador cruz tamaño mediano', 3990, 40, 1),

('HER003', 'Llave Inglesa', 'Llave ajustable 10 pulgadas', 12990, 15, 1);

--Tornillería
INSERT INTO productos
(codigo_producto, nombre, descripcion, precio, stock, id_categoria)
VALUES
('TOR001', 'Caja Tornillos 2"', 'Caja 100 unidades', 5990, 60, 2),

('TOR002', 'Tuercas Hexagonales', 'Pack 50 unidades', 3490, 80, 2),

('TOR003', 'Golillas Metálicas', 'Pack 100 unidades', 2490, 100, 2);

--Pinturas
INSERT INTO productos
(codigo_producto, nombre, descripcion, precio, stock, id_categoria)
VALUES
('PIN001', 'Pintura Blanca 1L', 'Pintura interior blanca mate', 8990, 20, 3),

('PIN002', 'Rodillo Pintura', 'Rodillo profesional', 4990, 35, 3),

('PIN003', 'Brocha 2"', 'Brocha mango madera', 2990, 50, 3);


--Electricidad
INSERT INTO productos
(codigo_producto, nombre, descripcion, precio, stock, id_categoria)
VALUES
('ELE001', 'Cable Eléctrico 10m', 'Cable aislado 220V', 15990, 12, 4),

('ELE002', 'Interruptor Simple', 'Interruptor pared blanco', 2490, 45, 4),

('ELE003', 'Ampolleta LED', 'Ampolleta 12W luz fría', 1990, 70, 4);

--Gasfitería
INSERT INTO productos
(codigo_producto, nombre, descripcion, precio, stock, id_categoria)
VALUES
('GAS001', 'Llave Paso', 'Llave paso metálica 1/2"', 6990, 22, 5),

('GAS002', 'Teflón', 'Cinta selladora gasfitería', 990, 100, 5),

('GAS003', 'Flexible Lavamanos', 'Flexible acero inoxidable', 5490, 30, 5);

--Seguridad
INSERT INTO productos
(codigo_producto, nombre, descripcion, precio, stock, id_categoria)
VALUES
('SEG001', 'Guantes Seguridad', 'Guantes anticorte talla M', 4990, 40, 6),

('SEG002', 'Lentes Protección', 'Lentes transparentes', 3990, 35, 6),

('SEG003', 'Casco Seguridad', 'Casco amarillo industrial', 12990, 18, 6);



-- Usuarios DEMO
INSERT INTO usuarios
(nombre_completo, correo, telefono, password_hash, rol)
VALUES
('Administrador Ferremas',
'admin@ferremas.cl',
'+56911111111',
'123456',
'ADMIN'),

('Juan Pérez',
'cliente@ferremas.cl',
'+56922222222',
'123456',
'CLIENTE');