import unittest
import sqlite3

from app import app
from test.test_setup import setup_in_memory_db
from test import mock_server
from modelo.producto_model import obtener_producto, actualizar_precio_usd


class TestCriteriosAceptacion(unittest.TestCase):
    """
    Pruebas de criterios de aceptaciÃ³n (CA).

    Validan que el sistema cumple las reglas de negocio definidas para Ferremas:
    precios vÃ¡lidos, conversiÃ³n correcta, autenticaciÃ³n segura, registro sin
    duplicados, rechazo de datos invÃ¡lidos y respuestas coherentes del mock externo.
    Ninguna prueba requiere levantar ferremas-api.
    """

    def setUp(self):
        import os
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

    # CA-001: Precio CLP del producto debe ser positivo
    def test_CA001_precio_cl_positivo(self):
        print('\n=== TEST: CA-001 - precio_cl_positivo ===')
        print('Criterio: todo producto en BD debe tener precio_cl > 0')
        producto = obtener_producto('HER001')
        print('Producto:', dict(producto) if producto else None)
        self.assertIsNotNone(producto)
        self.assertGreater(
            producto['precio_cl'], 0,
            'El precio en CLP debe ser mayor a cero'
        )
        print(f'precio_cl = {producto["precio_cl"]} â†’ CUMPLE criterio')

    # CA-002: Precio USD se calcula correctamente con la tasa de cambio
    def test_CA002_conversion_usd_correcta(self):
        print('\n=== TEST: CA-002 - conversion_usd_correcta ===')
        print('Criterio: precio_usd = round(precio_cl / tasa_cambio, 2)')
        tasa = 950.0
        actualizar_precio_usd('HER001', tasa)
        producto = obtener_producto('HER001')
        esperado = round(12000.0 / tasa, 2)
        obtenido = round(producto['precio_usd'], 2)
        print(f'precio_cl=12000, tasa={tasa} â†’ esperado={esperado}, obtenido={obtenido}')
        self.assertAlmostEqual(
            obtenido, esperado, places=2,
            msg='El precio USD no coincide con la conversiÃ³n esperada'
        )
        print('ConversiÃ³n USD â†’ CUMPLE criterio')

    # CA-003: Login con contraseÃ±a incorrecta debe ser rechazado (401)
    def test_CA003_login_credenciales_incorrectas_rechazado(self):
        print('\n=== TEST: CA-003 - login_credenciales_incorrectas_rechazado ===')
        payload = {'correo': 'juan@ejemplo.com', 'clave': 'WRONG_PASSWORD'}
        print('Criterio: acceso denegado si la contraseÃ±a no coincide')
        print('Request: POST /login ->', payload)
        respuesta = self.client.post('/login', json=payload)
        print('Response status:', respuesta.status_code)
        print('Response JSON:', respuesta.get_json())
        self.assertEqual(
            respuesta.status_code, 401,
            'El sistema debe retornar 401 con credenciales incorrectas'
        )
        print('Login rechazado correctamente â†’ CUMPLE criterio')

    # CA-004: Registro con correo ya existente debe fallar (400)
    def test_CA004_registro_correo_duplicado_rechazado(self):
        print('\n=== TEST: CA-004 - registro_correo_duplicado_rechazado ===')
        payload = {
            'nombre_completo': 'Clon Prueba',
            'correo': 'juan@ejemplo.com',  # correo ya insertado en test_setup
            'telefono': '+56900000000',
            'password': 'cualquiera'
        }
        print('Criterio: no se permite registrar dos usuarios con el mismo correo')
        print('Request: POST /registro ->', payload)
        respuesta = self.client.post('/registro', json=payload)
        print('Response status:', respuesta.status_code)
        print('Response JSON:', respuesta.get_json())
        self.assertEqual(
            respuesta.status_code, 400,
            'El sistema debe retornar 400 si el correo ya estÃ¡ registrado'
        )
        print('Correo duplicado rechazado â†’ CUMPLE criterio')

    # CA-005: Actualizar precios con tasa invÃ¡lida (0 o negativa) debe ser rechazado (400)
    def test_CA005_tasa_cambio_invalida_rechazada(self):
        print('\n=== TEST: CA-005 - tasa_cambio_invalida_rechazada ===')
        payload_cero = {'tasa_cambio': 0}
        print('Criterio: tasa_cambio <= 0 no es aceptable para cÃ¡lculo de precios')
        print('Request: POST /actualizar-precios-usd ->', payload_cero)
        respuesta = self.client.post('/actualizar-precios-usd', json=payload_cero)
        print('Response status:', respuesta.status_code)
        print('Response JSON:', respuesta.get_json())
        self.assertEqual(
            respuesta.status_code, 400,
            'El sistema debe rechazar tasa_cambio = 0'
        )
        print('Tasa invÃ¡lida rechazada â†’ CUMPLE criterio')

    # CA-006: Mock de divisa devuelve tasa numÃ©rica positiva (criterio de integraciÃ³n externa)
    def test_CA006_mock_divisa_retorna_tasa_valida(self):
        print('\n=== TEST: CA-006 - mock_divisa_retorna_tasa_valida ===')
        print('Criterio: el servicio de divisa (mindicador/banco central) debe retornar')
        print('          un valor numÃ©rico positivo para la tasa USD/CLP')
        resp = mock_server.app.test_client().get('/api/dolar')
        print('Response status:', resp.status_code)
        json_data = resp.get_json()
        print('Response JSON:', json_data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('serie', json_data)
        self.assertGreater(len(json_data['serie']), 0)
        valor = json_data['serie'][0]['valor']
        print(f'Tasa obtenida: {valor}')
        self.assertIsInstance(valor, (int, float), 'La tasa debe ser un nÃºmero')
        self.assertGreater(valor, 0, 'La tasa debe ser mayor a cero')
        print(f'Tasa = {valor} > 0 â†’ CUMPLE criterio')


if __name__ == '__main__':
    unittest.main()

