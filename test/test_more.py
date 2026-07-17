import unittest
import sqlite3
import os

from app import app
from test.test_setup import setup_in_memory_db
from modelo.producto_model import listar_productos_categoria, obtener_producto


class TestMore(unittest.TestCase):

    def setUp(self):
        # Crear DB en archivo temporal y parchear conectar
        self.db_path = setup_in_memory_db()
        import modelo.conexion as conexion
        self._orig_conectar = conexion.conectar

        def _conectar():
            c = sqlite3.connect(self.db_path, check_same_thread=False)
            c.row_factory = sqlite3.Row
            return c

        conexion.conectar = _conectar
        self.client = app.test_client()
        self.client.testing = True

    def tearDown(self):
        import modelo.conexion as conexion
        conexion.conectar = self._orig_conectar
        try:
            os.remove(self.db_path)
        except Exception:
            pass

    def test_actualizar_precio_individual_endpoint(self):
        print('\n=== TEST: actualizar_precio_individual_endpoint (integration) ===')
        payload = {'tasa_cambio': 1000.0}
        print('Request: POST /actualizar-precio-usd/HER001 ->', payload)
        # Llamar endpoint para actualizar precio individual
        resp = self.client.post('/actualizar-precio-usd/HER001', json=payload)
        print('Response status:', resp.status_code)
        data = resp.get_json()
        print('Response JSON:', data)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('producto', data)
        self.assertAlmostEqual(data['producto']['precio_usd'], 12.0, places=2)


if __name__ == '__main__':
    unittest.main()
