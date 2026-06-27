import unittest
from app import app


class TestIntegracion(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    # TI-001
    def test_endpoint_productos(self):
        respuesta = self.client.get("/productos")

        self.assertEqual(respuesta.status_code, 200)

        datos = respuesta.get_json()

        self.assertIsInstance(datos, list)
        self.assertGreater(len(datos), 0)

    # TI-002
    def test_endpoint_producto_individual(self):
        respuesta = self.client.get("/productos/HER001")

        self.assertEqual(respuesta.status_code, 200)

        producto = respuesta.get_json()

        self.assertEqual(producto["codigo_producto"], "HER001")
        self.assertEqual(producto["nombre"], "Martillo carpintero")


if __name__ == "__main__":
    unittest.main()