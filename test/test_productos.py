import unittest
import sqlite3

from modelo.producto_model import (
    obtener_productos,
    obtener_producto,
    listar_productos_categoria,
    actualizar_precio_usd,
    actualizar_todos_precios_usd
)

from test.test_setup import setup_in_memory_db



class TestProductos(unittest.TestCase):

    def setUp(self):
        # Crear DB en archivo temporal y parchear conectar para usarla
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

    def test_obtener_productos(self):
        print('\n=== TEST: obtener_productos (unit) ===')
        print('Calling: obtener_productos()')
        productos = obtener_productos()

        print('Result count:', len(productos) if productos is not None else 'None')
        print('Sample item:', dict(productos[0]) if productos else None)

        self.assertIsNotNone(productos)
        self.assertIsInstance(productos, list)
        self.assertGreater(len(productos), 0)

        primer_producto = productos[0]

        print('\nPrimer producto:')
        print(dict(primer_producto))

    def test_obtener_producto_existente(self):
        print('\n=== TEST: obtener_producto (unit) ===')
        print('Calling: obtener_producto("HER001")')

        producto = obtener_producto("HER001")

        print('Result:', dict(producto) if producto else None)

        self.assertIsNotNone(producto)

        self.assertEqual(
            producto["codigo_producto"],
            "HER001"
        )

        self.assertEqual(
            producto["nombre"],
            "Martillo carpintero"
        )



if __name__ == "__main__":
    unittest.main()