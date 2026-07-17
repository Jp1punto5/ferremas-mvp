import unittest

from test.test_setup import setup_in_memory_db

from modelo.producto_model import (
    listar_productos_categoria,
    actualizar_precio_usd,
    actualizar_todos_precios_usd,
    obtener_producto
)
from modelo.usuario_model import validar_login, registrar_usuario, obtener_usuario_por_correo


class TestExtras(unittest.TestCase):

    def setUp(self):
        import sqlite3, os
        self.db_path = setup_in_memory_db()
        import modelo.conexion as conexion
        self._orig_conectar = conexion.conectar

        def _conectar():
            c = sqlite3.connect(self.db_path, check_same_thread=False)
            c.row_factory = sqlite3.Row
            return c

        conexion.conectar = _conectar

    def tearDown(self):
        import modelo.conexion as conexion, os
        conexion.conectar = self._orig_conectar
        try:
            os.remove(self.db_path)
        except Exception:
            pass

    def test_listar_productos_categoria(self):
        print('\n=== TEST: listar_productos_categoria (unit) ===')
        print('Calling: listar_productos_categoria("Herramientas")')
        productos = listar_productos_categoria('Herramientas')
        print('Result count:', len(productos))
        print('First item:', productos[0])
        self.assertIsInstance(productos, list)
        self.assertGreater(len(productos), 0)
        self.assertEqual(productos[0]['categoria'], 'Herramientas')

    def test_actualizar_precio_usd(self):
        print('\n=== TEST: actualizar_precio_usd (unit) ===')
        print('Calling: actualizar_precio_usd("HER001", 1000.0)')
        # Actualizar precio de producto individual
        exito = actualizar_precio_usd('HER001', 1000.0)
        producto = obtener_producto('HER001')
        print('Updated product:', dict(producto) if producto else producto)
        self.assertTrue(exito)
        # precio_usd = round(precio_cl / tasa, 2) -> 12000 / 1000 = 12.0
        self.assertAlmostEqual(producto['precio_usd'], 12.0, places=2)

    def test_actualizar_todos_precios_usd(self):
        print('\n=== TEST: actualizar_todos_precios_usd (unit) ===')
        print('Calling: actualizar_todos_precios_usd(1000.0)')
        resultado = actualizar_todos_precios_usd(1000.0)
        print('Result:', resultado)
        self.assertTrue(resultado['success'])
        self.assertGreaterEqual(resultado['productos_actualizados'], 1)

    def test_validar_login_exitoso(self):
        print('\n=== TEST: validar_login (unit) ===')
        print('Calling: validar_login("juan@ejemplo.com", "secret")')
        # Usuario insertado en test_setup con correo 'juan@ejemplo.com' y password 'secret'
        usuario = validar_login('juan@ejemplo.com', 'secret')
        print('Result:', dict(usuario) if usuario else usuario)
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario['correo'], 'juan@ejemplo.com')


if __name__ == '__main__':
    unittest.main()
