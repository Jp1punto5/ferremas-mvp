Informe de trabajo: Tests y Mock - Ferremas MVP


Resumen ejecutivo
-----------------
Se implementó una suite de pruebas en `ferremas-mvp/test` con **27 tests activos** (unittest) más **3 escenarios Locust** (1 carga + 2 estrés). Cubre pruebas unitarias de backend y frontend, de integración, criterios de aceptación y mock de servicios externos (Webpay + mindicador/Banco Central).

IMPORTANTE: los 27 tests unittest NO requieren levantar ferremas-api ni ningún servicio externo.
Solo Locust necesita ferremas-api activo (puerto 5002).

Estado validado:
  python -m unittest discover -v  ->  Ran 27 tests in ~1.2s  OK

---

Distribucion de los 27 tests unittest
---------------------------------------
| #  | Test                                                  | Tipo                  | Archivo                      | Requiere ferremas-api |
|----|-------------------------------------------------------|-----------------------|------------------------------|-----------------------|
| 01 | test_obtener_productos                                | Unitario backend      | test_productos.py            | No                    |
| 02 | test_obtener_producto_existente                       | Unitario backend      | test_productos.py            | No                    |
| 03 | test_listar_productos_categoria                       | Unitario backend      | test_extra.py                | No                    |
| 04 | test_actualizar_precio_usd                            | Unitario backend      | test_extra.py                | No                    |
| 05 | test_actualizar_todos_precios_usd                     | Unitario backend      | test_extra.py                | No                    |
| 06 | test_validar_login_exitoso                            | Unitario backend      | test_extra.py                | No                    |
| 07 | test_FL001_mostrar_productos_filtra_stock_mayor_10    | Unitario frontend     | test_frontend_logica.py      | No                    |
| 08 | test_FL002_mostrar_productos_lista_vacia_sin_stock    | Unitario frontend     | test_frontend_logica.py      | No                    |
| 09 | test_FL003_resumen_sin_login_no_aplica_descuento      | Unitario frontend     | test_frontend_logica.py      | No                    |
| 10 | test_FL004_resumen_con_login_aplica_descuento_10%     | Unitario frontend     | test_frontend_logica.py      | No                    |
| 11 | test_endpoint_productos (TI-001)                      | Integracion           | test_integracion.py          | No                    |
| 12 | test_endpoint_producto_individual (TI-002)            | Integracion           | test_integracion.py          | No                    |
| 13 | test_endpoint_producto_no_existe (TI-003)             | Integracion           | test_integracion.py          | No                    |
| 14 | test_mock_obtener_dolar (TI-004)                      | Integracion/Mock      | test_integracion.py          | No                    |
| 15 | test_mock_webpay_init (TI-005)                        | Integracion/Mock      | test_integracion.py          | No                    |
| 16 | test_mock_webpay_commit (TI-006)                      | Integracion/Mock      | test_integracion.py          | No                    |
| 17 | test_endpoint_productos_por_categoria (TI-007)        | Integracion           | test_integracion.py          | No                    |
| 18 | test_endpoint_login_exitoso (TI-008)                  | Integracion           | test_integracion.py          | No                    |
| 19 | test_endpoint_categoria_no_existe (TI-009)            | Integracion           | test_integracion.py          | No                    |
| 20 | test_endpoint_registro_nuevo_usuario (TI-010)         | Integracion           | test_integracion.py          | No                    |
| 21 | test_actualizar_precio_individual_endpoint            | Integracion           | test_more.py                 | No                    |
| 22 | test_CA001_precio_cl_positivo                         | Criterio Aceptacion   | test_criterios_aceptacion.py | No                    |
| 23 | test_CA002_conversion_usd_correcta                    | Criterio Aceptacion   | test_criterios_aceptacion.py | No                    |
| 24 | test_CA003_login_credenciales_incorrectas_rechazado   | Criterio Aceptacion   | test_criterios_aceptacion.py | No                    |
| 25 | test_CA004_registro_correo_duplicado_rechazado        | Criterio Aceptacion   | test_criterios_aceptacion.py | No                    |
| 26 | test_CA005_tasa_cambio_invalida_rechazada             | Criterio Aceptacion   | test_criterios_aceptacion.py | No                    |
| 27 | test_CA006_mock_divisa_retorna_tasa_valida            | Criterio Aceptacion   | test_criterios_aceptacion.py | No                    |

Pruebas de carga y estres (Locust) — 3 escenarios — REQUIEREN ferremas-api
---------------------------------------------------------------------------
| #  | Clase                  | Escenario             | Usuarios | Wait time    | Resultado                |
|----|------------------------|-----------------------|----------|--------------|--------------------------|
| L1 | FerremasCargarUser     | Carga normal          | u=50     | 1–3 s        | ESTABLE (evidencia real) |
| E1 | FerremasEstres1User    | Estres catalogo       | u=350    | 0.1–0.5 s    | QUIEBRE en u=350         |
| E2 | FerremasEstres2User    | Estres flujo checkout | u=350    | 0.05–0.3 s   | QUIEBRE TOTAL en u=350   |

---

Cambios principales realizados
-------------------------------------------
1) Mock HTTP (test/mock_server.py)
   - Endpoints simulados:
     - GET /api/dolar -> estructura tipo mindicador.cl (Banco Central)
     - POST /webpay/init -> crea token_ws + url
     - POST /webpay/commit -> confirma transaccion (AUTHORIZED)
   - Los tests usan `mock_server.app.test_client()` internamente; no requiere proceso separado.
   - NO reemplaza a ferremas-api para el navegador — solo para tests automaticos.

2) Base de datos de pruebas (SQLite temporal)
   - `ferremas-mvp/test/test_setup.py` crea un archivo temporal con esquema y datos de ejemplo.
   - Los tests parchean `modelo.conexion.conectar` para apuntar al archivo temporal.
   - La BD real (productiva) vive en `ferremas-api/modelo/`.

3) Migracion de logica productiva de BD a ferremas-api
   - Se canonizo el componente `modelo/` en `ferremas-api/modelo/` (conexion, modelos, init_db, SQL).
   - Se expusieron en `ferremas-api/app.py` todas las rutas de productos/usuarios.
   - En `ferremas-mvp/modelo/` se mantiene scaffolding de pruebas (shims que parchean los tests).

4) Estrategia oficial de carga/estres con Locust
   - `test/locustfile.py` es el artefacto oficial de benchmarking.
   - 3 clases: FerremasCargarUser (L1), FerremasEstres1User (E1), FerremasEstres2User (E2).
   - Evidencias en `test/resultados/`: run_L1_*, run_E1_*, run_E2_*.
   - Error en quiebre: WinError 10048 (agotamiento de puertos/sockets en Windows).
   - Los archivos `test_carga.py` y `test_estres.py` fueron eliminados (eran obsoletos).

5) Criterio de quiebre para informe
   - error% >= 1% O p95 >= 2000ms -> sistema fuera de umbral.
   - Limite practico: u=50 (cumple). Quiebre: u=350 (no cumple).

---

Prueba de carga — tabla para informe
-----------------------------------------
| Escenario | Concurrentes | RPS    | p50 (ms) | p95 (ms) | Error %  | Estado        |
|-----------|--------------|--------|----------|----------|----------|---------------|
| L1        | 50           | 105.54 | 9        | 36       | 0.000    | ESTABLE       |
| E1        | 350          | 276.05 | 110      | 2900     | 3.978    | QUIEBRE       |
| E2        | 350          | 84.34  | 2000     | 7200     | 68.594   | QUIEBRE TOTAL |

Nota E2: WinError 10061 en todos los endpoints (crash de ferremas-api bajo 350u en checkout).
Crash iniciado en segundo 88. Limite practico checkout: <= 50 usuarios concurrentes.

Comandos oficiales (terminal integrada VS Code, CMD):
  venv\Scripts\activate.bat
  python -m locust -f test/locustfile.py --headless -u 50  -r 5  --run-time 90s --host http://127.0.0.1:5002 --csv test/resultados/run_L1 FerremasCargarUser
  python -m locust -f test/locustfile.py --headless -u 350 -r 10 --run-time 90s --host http://127.0.0.1:5002 --csv test/resultados/run_E1 FerremasEstres1User
  python -m locust -f test/locustfile.py --headless -u 350 -r 10 --run-time 90s --host http://127.0.0.1:5002 --csv test/resultados/run_E2 FerremasEstres2User

Detener antes del tiempo: Ctrl+C

---

Notas tecnicas
--------------
- Los criterios de aceptacion (CA-001 a CA-006) NO requieren ferremas-api.
- ResourceWarning de sqlite en algunos tests: cosmetica, no afecta resultados.
- Usar siempre `python -m pip` (no `pip`) en Windows con el venv de este proyecto.
- Locust ya esta en requirements.txt; no se requiere instalacion adicional.

---

Ubicacion de archivos relevantes
---------------------------------
ferremas-mvp/
  test/
    test_productos.py         (2 tests unitarios backend)
    test_extra.py             (4 tests unitarios backend)
    test_frontend_logica.py   (4 tests unitarios frontend FL-001 a FL-004)
    test_integracion.py       (10 tests de integracion TI-001 a TI-010)
    test_more.py              (1 test de integracion)
    test_criterios_aceptacion.py  (6 criterios de aceptacion CA-001 a CA-006)
    mock_server.py            (mock Webpay + divisa/mindicador)
    test_setup.py             (DB SQLite temporal)
    locustfile.py             (3 escenarios Locust: L1, E1, E2)
    resultados/               (CSVs run_L1_*, run_E1_*, run_E2_*, EVIDENCIA_CARGA_ESTRES.txt)
    README.md                 (guia de ejecucion)
    DESCRIPCION_TESTS.md      (detalle de cada test)
    TESTS_REPORT.md           (este documento)
    CONTEXTO_PARA_CHATGPT.md  (contexto completo para informe)

ferremas-api/
  modelo/                     (BD real — productiva)
  app.py                      (todas las rutas: productos, usuarios, divisa, webpay)

---

Ejecucion rapida
-----------------
  cd ferremas-mvp
  python -m unittest discover -v
  -> Ran 27 tests in ~1.2s  OK
