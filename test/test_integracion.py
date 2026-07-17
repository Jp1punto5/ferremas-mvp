import unittest
from app import app
from test.test_setup import setup_in_memory_db
from test import mock_server


class TestIntegracion(unittest.TestCase):

    def setUp(self):
        # Preparar DB en archivo temporal y parchear conectar antes de crear el test_client
        import sqlite3, os
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
        import modelo.conexion as conexion, os
        conexion.conectar = self._orig_conectar
        try:
            os.remove(self.db_path)
        except Exception:
            pass

    # TI-001
    def test_endpoint_productos(self):
        print('\n=== TEST: TI-001 - endpoint_productos (GET /productos) ===')
        print('Request: GET /productos')
        respuesta = self.client.get("/productos")

        print('Response status:', respuesta.status_code)
        datos = respuesta.get_json()
        print('Response JSON:', datos)

        self.assertEqual(respuesta.status_code, 200)

        self.assertIsInstance(datos, list)
        self.assertGreater(len(datos), 0)

    # TI-002
    def test_endpoint_producto_individual(self):
        print('\n=== TEST: TI-002 - endpoint_producto_individual (GET /productos/HER001) ===')
        print('Request: GET /productos/HER001')
        respuesta = self.client.get("/productos/HER001")

        print('Response status:', respuesta.status_code)
        producto = respuesta.get_json()
        print('Response JSON:', producto)

        self.assertEqual(respuesta.status_code, 200)

        self.assertEqual(producto["codigo_producto"], "HER001")
        self.assertEqual(producto["nombre"], "Martillo carpintero")

    # TI-003 (producto no existente)
    def test_endpoint_producto_no_existe(self):
        print('\n=== TEST: TI-003 - endpoint_producto_no_existe (GET /productos/NOEXIST) ===')
        print('Request: GET /productos/NOEXIST')
        respuesta = self.client.get("/productos/NOEXIST")
        print('Response status:', respuesta.status_code)
        print('Response JSON:', respuesta.get_json())
        self.assertEqual(respuesta.status_code, 404)

    # TI-004 - Obtener tasa desde mock (banco central / mindicador)
    def test_mock_obtener_dolar(self):
        print('\n=== TEST: TI-004 - mock_obtener_dolar (GET /api/dolar) ===')
        print('Request: GET /api/dolar (mock)')
        resp = mock_server.app.test_client().get('/api/dolar')
        print('Response status:', resp.status_code)
        json_data = resp.get_json()
        print('Response JSON:', json_data)
        self.assertEqual(resp.status_code, 200)
        # estructura esperada: { serie: [ { fecha, valor } ] }
        self.assertIn('serie', json_data)
        self.assertGreater(len(json_data['serie']), 0)

    # TI-005 - Crear transacción Webpay (mock)
    def test_mock_webpay_init(self):
        print('\n=== TEST: TI-005 - mock_webpay_init (POST /webpay/init) ===')
        payload = {
            'buy_order': 'ORD_TEST',
            'session_id': 'SESS_TEST',
            'amount': 10000,
            'return_url': 'http://localhost/return'
        }
        print('Request JSON:', payload)
        resp = mock_server.app.test_client().post('/webpay/init', json=payload)
        print('Response status:', resp.status_code)
        json_data = resp.get_json()
        print('Response JSON:', json_data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('token_ws', json_data)
        self.assertIn('url', json_data)

    # TI-006 - Commit/confirmación Webpay (mock)
    def test_mock_webpay_commit(self):
        print('\n=== TEST: TI-006 - mock_webpay_commit (POST /webpay/commit) ===')
        # primero obtener token
        resp_init = mock_server.app.test_client().post('/webpay/init', json={'buy_order': 'ORD2', 'session_id': 'S2', 'amount': 5000, 'return_url': 'http://localhost/return'})
        token = resp_init.get_json().get('token_ws')
        print('Using token:', token)
        # confirmar
        resp = mock_server.app.test_client().post('/webpay/commit', data={'token_ws': token})
        print('Response status:', resp.status_code)
        json_data = resp.get_json()
        print('Response JSON:', json_data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json_data.get('status'), 'AUTHORIZED')

    # TI-007 - Endpoint productos por categoría
    def test_endpoint_productos_por_categoria(self):
        print('\n=== TEST: TI-007 - endpoint_productos_por_categoria (GET /productos/categoria/Herramientas) ===')
        print('Request: GET /productos/categoria/Herramientas')
        respuesta = self.client.get("/productos/categoria/Herramientas")
        print('Response status:', respuesta.status_code)
        datos = respuesta.get_json()
        print('Response JSON:', datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIsInstance(datos, list)
        self.assertGreater(len(datos), 0)
        self.assertEqual(datos[0]['categoria'], 'Herramientas')

    # TI-008 - Endpoint login con credenciales correctas
    def test_endpoint_login_exitoso(self):
        print('\n=== TEST: TI-008 - endpoint_login_exitoso (POST /login) ===')
        payload = {'correo': 'juan@ejemplo.com', 'clave': 'secret'}
        print('Request: POST /login ->', payload)
        respuesta = self.client.post('/login', json=payload)
        print('Response status:', respuesta.status_code)
        datos = respuesta.get_json()
        print('Response JSON:', datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertTrue(datos.get('success'))
        self.assertIn('usuario', datos)

    # TI-009 - Categoría inexistente retorna lista vacía
    def test_endpoint_categoria_no_existe(self):
        print('\n=== TEST: TI-009 - endpoint_categoria_no_existe (GET /productos/categoria/INVALIDA) ===')
        print('Request: GET /productos/categoria/INVALIDA')
        respuesta = self.client.get("/productos/categoria/INVALIDA")
        print('Response status:', respuesta.status_code)
        datos = respuesta.get_json()
        print('Response JSON:', datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIsInstance(datos, list)
        self.assertEqual(len(datos), 0)

    # TI-010 - Registro de nuevo usuario
    def test_endpoint_registro_nuevo_usuario(self):
        print('\n=== TEST: TI-010 - endpoint_registro_nuevo_usuario (POST /registro) ===')
        payload = {
            'nombre_completo': 'Maria Prueba',
            'correo': 'maria@ejemplo.com',
            'telefono': '+56987654321',
            'password': 'clave123'
        }
        print('Request: POST /registro ->', payload)
        respuesta = self.client.post('/registro', json=payload)
        print('Response status:', respuesta.status_code)
        datos = respuesta.get_json()
        print('Response JSON:', datos)
        self.assertEqual(respuesta.status_code, 201)
        self.assertTrue(datos.get('success'))


if __name__ == "__main__":
    unittest.main()