# Descripcion detallada de pruebas (ferremas-mvp/test)

## Estado actual

- Suite `unittest` activa: **27 tests** (`python -m unittest discover -v`)
- Carga y estres oficiales: **Locust** — 3 escenarios (`test/locustfile.py`)
- Evidencias actuales de carga/estres: `test/resultados/`

---

## 1) Tests unitarios y de integracion (unittest) — 27 tests

### Archivo: `test_productos.py`

1. `test_obtener_productos`
   - Para que sirve: validar listado de productos desde modelo.
   - Que verifica: retorna lista no vacia, tipo correcto y estructura de producto.
   - Como se ejecuta:
     - `python -m unittest test.test_productos.TestProductos.test_obtener_productos`

2. `test_obtener_producto_existente`
   - Para que sirve: validar obtencion de producto por codigo.
   - Que verifica: codigo `HER001` y nombre `Martillo carpintero`.
   - Como se ejecuta:
     - `python -m unittest test.test_productos.TestProductos.test_obtener_producto_existente`

### Archivo: `test_frontend_logica.py` — Logica de frontend (FL)

Validan las **reglas de negocio implementadas en el JavaScript** del frontend.
Como Node.js no esta disponible en este entorno, se extrajo la logica pura de las
funciones JS y se testea en Python. Verifica exactamente las mismas reglas que el
navegador ejecuta.

**Funciones testeadas:**
- `mostrarProductos(productos)` en `vista/js/cargar_imagen.js`
- `mostrarResumenCompra()` en `vista/js/carrito.js`

7. `test_FL001_mostrar_productos_filtra_stock_mayor_10`
   - Para que sirve: validar que `mostrarProductos` solo renderiza productos con stock <= 10.
   - Que verifica: productos con stock > 10 quedan fuera; stock = 10 es el borde inclusivo.
   - Logica JS: `if(producto.stock <= 10) { renderizar tarjeta }`
   - Como se ejecuta:
     - `python -m unittest test.test_frontend_logica.TestFrontendLogica.test_FL001_mostrar_productos_filtra_stock_mayor_10`

8. `test_FL002_mostrar_productos_lista_vacia_si_todo_sin_stock`
   - Para que sirve: validar que si todos los productos tienen stock > 10, el grid queda vacio.
   - Que verifica: lista de visibles = [] cuando todo supera el umbral.
   - Como se ejecuta:
     - `python -m unittest test.test_frontend_logica.TestFrontendLogica.test_FL002_mostrar_productos_lista_vacia_si_todo_sin_stock`

9. `test_FL003_resumen_sin_login_no_aplica_descuento`
   - Para que sirve: validar que `mostrarResumenCompra` NO aplica descuento sin usuario logeado.
   - Que verifica: total_final == total_bruto (descuento = 0).
   - Logica JS: `if(usuarioLogeado) { descuento = total * 0.10 }`
   - Como se ejecuta:
     - `python -m unittest test.test_frontend_logica.TestFrontendLogica.test_FL003_resumen_sin_login_no_aplica_descuento`

10. `test_FL004_resumen_con_login_aplica_descuento_10_porciento`
    - Para que sirve: validar que con usuario logeado se aplica exactamente el 10% de descuento.
    - Que verifica: descuento = total * 0.10 y total_final = total - descuento.
    - Como se ejecuta:
      - `python -m unittest test.test_frontend_logica.TestFrontendLogica.test_FL004_resumen_con_login_aplica_descuento_10_porciento`

### Archivo: `test_extra.py`

11. `test_listar_productos_categoria`
   - Para que sirve: validar filtro por categoria.
   - Que verifica: categoria `Herramientas` con al menos 1 resultado.
   - Como se ejecuta:
     - `python -m unittest test.test_extra.TestExtras.test_listar_productos_categoria`

4. `test_actualizar_precio_usd`
   - Para que sirve: validar actualizacion de precio USD de 1 producto.
   - Que verifica: `HER001` queda en `12.0` con tasa `1000.0`.
   - Como se ejecuta:
     - `python -m unittest test.test_extra.TestExtras.test_actualizar_precio_usd`

5. `test_actualizar_todos_precios_usd`
   - Para que sirve: validar actualizacion masiva de precios USD.
   - Que verifica: `success=True` y `productos_actualizados >= 1`.
   - Como se ejecuta:
     - `python -m unittest test.test_extra.TestExtras.test_actualizar_todos_precios_usd`

6. `test_validar_login_exitoso`
   - Para que sirve: validar login con usuario de prueba.
   - Que verifica: correo `juan@ejemplo.com` y credenciales correctas.
   - Como se ejecuta:
     - `python -m unittest test.test_extra.TestExtras.test_validar_login_exitoso`

### Archivo: `test_integracion.py`

7. `test_endpoint_productos` (TI-001)
   - Para que sirve: validar endpoint de listado de productos.
   - Que verifica: `GET /productos` responde 200 y lista.
   - Como se ejecuta:
     - `python -m unittest test.test_integracion.TestIntegracion.test_endpoint_productos`

8. `test_endpoint_producto_individual` (TI-002)
   - Para que sirve: validar endpoint de producto por codigo.
   - Que verifica: `GET /productos/HER001` responde 200 y datos correctos.
   - Como se ejecuta:
     - `python -m unittest test.test_integracion.TestIntegracion.test_endpoint_producto_individual`

9. `test_endpoint_producto_no_existe` (TI-003)
   - Para que sirve: validar manejo de producto inexistente.
   - Que verifica: `GET /productos/NOEXIST` responde 404.
   - Como se ejecuta:
     - `python -m unittest test.test_integracion.TestIntegracion.test_endpoint_producto_no_existe`

10. `test_mock_obtener_dolar` (TI-004)
    - Para que sirve: validar mock de divisa/mindicador.
    - Que verifica: `GET /api/dolar` (mock) responde 200 con `serie`.
    - Como se ejecuta:
      - `python -m unittest test.test_integracion.TestIntegracion.test_mock_obtener_dolar`

11. `test_mock_webpay_init` (TI-005)
    - Para que sirve: validar inicio de transaccion Webpay mock.
    - Que verifica: `POST /webpay/init` devuelve `token_ws` y `url`.
    - Como se ejecuta:
      - `python -m unittest test.test_integracion.TestIntegracion.test_mock_webpay_init`

12. `test_mock_webpay_commit` (TI-006)
    - Para que sirve: validar confirmacion de pago Webpay mock.
    - Que verifica: `POST /webpay/commit` devuelve `status=AUTHORIZED`.
    - Como se ejecuta:
      - `python -m unittest test.test_integracion.TestIntegracion.test_mock_webpay_commit`

13. `test_endpoint_productos_por_categoria` (TI-007)
    - Para que sirve: validar endpoint de productos filtrados por categoria.
    - Que verifica: `GET /productos/categoria/Herramientas` responde 200, lista con al menos 1 item y categoria correcta.
    - Como se ejecuta:
      - `python -m unittest test.test_integracion.TestIntegracion.test_endpoint_productos_por_categoria`

14. `test_endpoint_login_exitoso` (TI-008)
    - Para que sirve: validar endpoint de login con credenciales correctas.
    - Que verifica: `POST /login` responde 200, `success=True` y devuelve `usuario`.
    - Como se ejecuta:
      - `python -m unittest test.test_integracion.TestIntegracion.test_endpoint_login_exitoso`

15. `test_endpoint_categoria_no_existe` (TI-009)
    - Para que sirve: validar que una categoria inexistente devuelve lista vacia.
    - Que verifica: `GET /productos/categoria/INVALIDA` responde 200 y lista vacia `[]`.
    - Como se ejecuta:
      - `python -m unittest test.test_integracion.TestIntegracion.test_endpoint_categoria_no_existe`

16. `test_endpoint_registro_nuevo_usuario` (TI-010)
    - Para que sirve: validar registro exitoso de un nuevo usuario.
    - Que verifica: `POST /registro` con datos nuevos responde 201 y `success=True`.
    - Como se ejecuta:
      - `python -m unittest test.test_integracion.TestIntegracion.test_endpoint_registro_nuevo_usuario`

### Archivo: `test_more.py`

17. `test_actualizar_precio_individual_endpoint`
    - Para que sirve: validar endpoint de actualizacion individual de precio USD.
    - Que verifica: `POST /actualizar-precio-usd/HER001` responde 200 y precio USD esperado.
    - Como se ejecuta:
      - `python -m unittest test.test_more.TestMore.test_actualizar_precio_individual_endpoint`

---

## 3) Pruebas de criterios de aceptacion (CA)

Validan que el sistema cumple las **reglas de negocio** definidas para Ferremas.
No solo verifican status codes — comprueban que los datos y la logica son correctos segun los requisitos del sistema.

### Archivo: `test_criterios_aceptacion.py`

18. `test_CA001_precio_cl_positivo`
    - Para que sirve: garantizar que todo producto tiene precio en CLP mayor a cero.
    - Que verifica: `producto['precio_cl'] > 0` (regla de negocio: precio siempre positivo).
    - Como se ejecuta:
      - `python -m unittest test.test_criterios_aceptacion.TestCriteriosAceptacion.test_CA001_precio_cl_positivo`

19. `test_CA002_conversion_usd_correcta`
    - Para que sirve: validar que la conversion USD/CLP es matematicamente correcta.
    - Que verifica: `precio_usd == round(precio_cl / tasa_cambio, 2)`.
    - Como se ejecuta:
      - `python -m unittest test.test_criterios_aceptacion.TestCriteriosAceptacion.test_CA002_conversion_usd_correcta`

20. `test_CA003_login_credenciales_incorrectas_rechazado`
    - Para que sirve: garantizar que el sistema rechaza acceso con contrasena incorrecta.
    - Que verifica: `POST /login` con clave incorrecta responde 401 (no autorizado).
    - Como se ejecuta:
      - `python -m unittest test.test_criterios_aceptacion.TestCriteriosAceptacion.test_CA003_login_credenciales_incorrectas_rechazado`

21. `test_CA004_registro_correo_duplicado_rechazado`
    - Para que sirve: garantizar que no se permiten dos usuarios con el mismo correo.
    - Que verifica: `POST /registro` con correo ya existente responde 400.
    - Como se ejecuta:
      - `python -m unittest test.test_criterios_aceptacion.TestCriteriosAceptacion.test_CA004_registro_correo_duplicado_rechazado`

22. `test_CA005_tasa_cambio_invalida_rechazada`
    - Para que sirve: garantizar que una tasa de cambio invalida (0 o negativa) es rechazada.
    - Que verifica: `POST /actualizar-precios-usd` con `tasa_cambio=0` responde 400.
    - Como se ejecuta:
      - `python -m unittest test.test_criterios_aceptacion.TestCriteriosAceptacion.test_CA005_tasa_cambio_invalida_rechazada`

23. `test_CA006_mock_divisa_retorna_tasa_valida`
    - Para que sirve: validar que el servicio de divisa (mindicador/banco central) retorna un valor util para el sistema.
    - Que verifica: el mock responde 200 con `serie[0]['valor']` numerico y positivo.
    - Como se ejecuta:
      - `python -m unittest test.test_criterios_aceptacion.TestCriteriosAceptacion.test_CA006_mock_divisa_retorna_tasa_valida`

---

## 2) Pruebas de carga y estres (oficial: Locust)

> **Locust SI requiere ferremas-api activo** (puerto 5002). Es el unico componente de toda la suite que necesita un servicio levantado.

- Archivo: `test/locustfile.py`
- Host objetivo: `http://127.0.0.1:5002` (ferremas-api)

### Escenarios disponibles

| Clase Locust          | Escenario            | Endpoints                       | Wait time  | Usuarios |
|-----------------------|----------------------|---------------------------------|------------|----------|
| `FerremasCargarUser`  | L1 — Carga normal    | /productos, /categoria, /codigo | 1–3 s      | u=50     |
| `FerremasEstres1User` | E1 — Estres catalogo | /productos, /categoria, /codigo | 0.1–0.5 s  | u=350    |
| `FerremasEstres2User` | E2 — Estres checkout | /productos, /login, /checkout   | 0.05–0.3 s | u=350    |

### Ejecucion

Desde terminal integrada VS Code (CMD), con venv activo y ferremas-api levantado:

```bash
venv\Scripts\activate.bat

# Selector interactivo de escenario (recomendado):
python -m locust -f test/locustfile.py --class-picker

# O ejecutar un escenario especifico en headless:
python -m locust -f test/locustfile.py --class-picker --headless -u 50  -r 5  --run-time 90s --host http://127.0.0.1:5002 --csv test/resultados/run_L1
python -m locust -f test/locustfile.py --class-picker --headless -u 350 -r 10 --run-time 90s --host http://127.0.0.1:5002 --csv test/resultados/run_E1
python -m locust -f test/locustfile.py --class-picker --headless -u 350 -r 10 --run-time 90s --host http://127.0.0.1:5002 --csv test/resultados/run_E2
```

> Locust ya esta incluido en `requirements.txt`. No se requiere instalacion adicional.

> Para detener antes del tiempo: `Ctrl+C`.

### Criterio de quiebre

- **ESTABLE**: error% < 1% y p95 < 2000 ms
- **QUIEBRE**: error% >= 1% o p95 >= 2000 ms

### Evidencias guardadas en test/resultados/

| Archivo                      | Escenario            | error% | p95     | Estado            |
|------------------------------|----------------------|--------|---------|-------------------|
| `run_L1_stats.csv`           | L1 — 50u             | 0.000% | 36 ms   | ESTABLE           |
| `run_E1_stats.csv`           | E1 — 350u            | 3.978% | 2900 ms | QUIEBRE           |
| `run_E2_stats.csv`           | E2 — 350u (checkout) | 20.13% | 6600 ms | QUIEBRE SEVERO    |
| `EVIDENCIA_CARGA_ESTRES.txt` | **Todos**            | ------ | ------- | Analisis completo |

- Error relevante observado en E1/E2: `WinError 10048` — agotamiento de sockets en Windows.
- run_u50_* y run_u350_* tambien conservados (equivalentes a L1 y E1 respectivamente).

---

## Resumen de cobertura total

| #  | Test                                                       | Tipo                | Archivo                      |
|----|------------------------------------------------------------|---------------------|------------------------------|
| 1  | test_obtener_productos                                     | Unitario            | test_productos.py            |
| 2  | test_obtener_producto_existente                            | Unitario            | test_productos.py            |
| 3  | test_FL001_mostrar_productos_filtra_stock_mayor_10         | Unitario Frontend   | test_frontend_logica.py      |
| 4  | test_FL002_mostrar_productos_lista_vacia_si_todo_sin_stock | Unitario Frontend   | test_frontend_logica.py      |
| 5  | test_FL003_resumen_sin_login_no_aplica_descuento           | Unitario Frontend   | test_frontend_logica.py      |
| 6  | test_FL004_resumen_con_login_aplica_descuento_10_porciento | Unitario Frontend   | test_frontend_logica.py      |
| 7  | test_listar_productos_categoria                            | Unitario            | test_extra.py                |
| 8  | test_actualizar_precio_usd                                 | Unitario            | test_extra.py                |
| 9  | test_actualizar_todos_precios_usd                          | Unitario            | test_extra.py                |
| 10 | test_validar_login_exitoso                                 | Unitario            | test_extra.py                |
| 11 | test_endpoint_productos (TI-001)                           | Integracion         | test_integracion.py          |
| 12 | test_endpoint_producto_individual (TI-002)                 | Integracion         | test_integracion.py          |
| 13 | test_endpoint_producto_no_existe (TI-003)                  | Integracion         | test_integracion.py          |
| 14 | test_mock_obtener_dolar (TI-004)                           | Integracion/Mock    | test_integracion.py          |
| 15 | test_mock_webpay_init (TI-005)                             | Integracion/Mock    | test_integracion.py          |
| 16 | test_mock_webpay_commit (TI-006)                           | Integracion/Mock    | test_integracion.py          |
| 17 | test_endpoint_productos_por_categoria (TI-007)             | Integracion         | test_integracion.py          |
| 18 | test_endpoint_login_exitoso (TI-008)                       | Integracion         | test_integracion.py          |
| 19 | test_endpoint_categoria_no_existe (TI-009)                 | Integracion         | test_integracion.py          |
| 20 | test_endpoint_registro_nuevo_usuario (TI-010)              | Integracion         | test_integracion.py          |
| 21 | test_actualizar_precio_individual_endpoint                 | Integracion         | test_more.py                 |
| 22 | test_CA001_precio_cl_positivo                              | Criterio Aceptacion | test_criterios_aceptacion.py |
| 23 | test_CA002_conversion_usd_correcta                         | Criterio Aceptacion | test_criterios_aceptacion.py |
| 24 | test_CA003_login_credenciales_incorrectas_rechazado        | Criterio Aceptacion | test_criterios_aceptacion.py |
| 25 | test_CA004_registro_correo_duplicado_rechazado             | Criterio Aceptacion | test_criterios_aceptacion.py |
| 26 | test_CA005_tasa_cambio_invalida_rechazada                  | Criterio Aceptacion | test_criterios_aceptacion.py |
| 27 | test_CA006_mock_divisa_retorna_tasa_valida                 | Criterio Aceptacion | test_criterios_aceptacion.py |
| L1 | FerremasCargarUser (carga normal, u=50)                    | Carga               | locustfile.py                |
| E1 | FerremasEstres1User (estres catalogo, u=200-350)           | Estres              | locustfile.py                |
| E2 | FerremasEstres2User (estres checkout, u=350)               | Estres              | locustfile.py                |

