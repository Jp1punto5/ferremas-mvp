import unittest

from modelo.producto_model import obtener_productos, obtener_producto


class TestProductos(unittest.TestCase):

    def test_obtener_productos(self):
        productos = obtener_productos()

        self.assertIsNotNone(productos)
        self.assertIsInstance(productos, list)
        self.assertGreater(len(productos), 0)

        primer_producto = productos[0]

        print("\nPrimer producto:")
        print(dict(primer_producto))

    def test_obtener_producto_existente(self):

        producto = obtener_producto("HER001")

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