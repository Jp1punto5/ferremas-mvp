# Pruebas de Software - Ferremas MVP

Esta carpeta contiene los archivos utilizados para validar el correcto funcionamiento del sistema **Ferremas-MVP**, incluyendo pruebas unitarias, de integración, Mock, carga y estrés.

## Requisitos

Antes de ejecutar cualquiera de las pruebas, asegúrese de:

1. Clonar el repositorio.
2. Crear y activar el entorno virtual.
3. Instalar las dependencias del proyecto:

```bash
python -m pip install -r requirements.txt
```

> Locust ya está incluido en `requirements.txt`. No se necesita instalación adicional.

---

## Resumen de tests incluidos

**27 tests unittest + 3 escenarios Locust. Ningún unittest requiere levantar ferremas-api.**

| Tipo                                 | Cantidad     | Archivo                           |
|--------------------------------------|--------------|-----------------------------------|
| Unitarios backend (modelo)           |    6         | test_productos.py, test_extra.py  |
| Unitarios frontend (lógica JS)       |    4         | test_frontend_logica.py           |
| Integración (endpoints Flask + mock) |   11         | test_integracion.py, test_more.py |
| Criterios de aceptación              |    6         | test_criterios_aceptacion.py      |
| **Total unittest**                   | **27**       | **------------------------------**|
| Carga/estrés Locust                  | 3 escenarios | locustfile.py                     |


## Ubicación del código de la base de datos (estado actual)

- La implementación productiva del componente `modelo/` está en `ferremas-api/modelo/`. Esa es la fuente de verdad para la BD real en producción.

- Las pruebas automáticas usan `ferremas-mvp/test/test_setup.py`, que crea y siembra una base de datos SQLite temporal por cada test. Durante los tests la función `modelo.conexion.conectar` es parcheada automáticamente para apuntar a ese archivo temporal.

- **Resultado práctico: los 27 tests unittest NO requieren levantar ferremas-api ni ningún otro servicio.**

---

## ¿Los criterios de aceptación necesitan ferremas-api?

**No.** Los 6 tests CA (CA-001 a CA-006) usan:
- `app.test_client()` — Flask test client interno (sin abrir ningún puerto)
- SQLite temporal parcheada (sin tocar la BD real)
- `mock_server.app.test_client()` para CA-006 (divisa, también en memoria)

Ninguno de los 27 tests hace llamadas HTTP al puerto 5002.

---

> Los archivos `test_carga.py` y `test_estres.py` han sido **eliminados**. La herramienta oficial para pruebas de carga y estrés es **Locust** (`test/locustfile.py`).

---

## Ejecutar la suite completa (unittest — 27 tests)

Desde la carpeta `ferremas-mvp`:

```bash
python -m unittest discover -v
```

Resultado esperado: `Ran 27 tests in ~1.2s  OK`

Para ejecutar un tipo específico:

```bash
python -m unittest test.test_productos          # 2 unitarios backend
python -m unittest test.test_extra              # 4 unitarios backend
python -m unittest test.test_frontend_logica    # 4 unitarios frontend (FL)
python -m unittest test.test_integracion        # 10 integracion (TI-001 a TI-010)
python -m unittest test.test_more               # 1 integracion (precio USD individual)
python -m unittest test.test_criterios_aceptacion  # 6 criterios de aceptacion (CA)
```

## Ejecución oficial de carga/estrés con Locust

> Locust **sí requiere ferremas-api activo** (puerto 5002). Es el único componente que necesita un servicio levantado.

### Paso a paso (Terminal integrada de VS Code — CMD)

> Usar CMD o Bash integrado de VS Code. No PowerShell.

1) En una terminal, levantar `ferremas-api`:
```bash
cd ferremas-api
venv\Scripts\activate.bat
python app.py
```

2) En otra terminal, ubicarse en `ferremas-mvp` y activar venv:
```bash
cd ferremas-mvp
venv\Scripts\activate.bat
```

3) Elegir escenario con el selector interactivo:
```bash
python -m locust -f test/locustfile.py --class-picker
```

O ejecutar un escenario específico en modo headless:

**Escenario L1 — Carga normal (50 usuarios, sistema estable):**
```bash
python -m locust -f test/locustfile.py --class-picker --headless -u 50 -r 5 --run-time 90s --host http://127.0.0.1:5002 --csv test/resultados/run_L1
```

**Escenario E1 — Estrés catálogo (350 usuarios, detecta límite):**
```bash
python -m locust -f test/locustfile.py --class-picker --headless -u 350 -r 10 --run-time 90s --host http://127.0.0.1:5002 --csv test/resultados/run_E1
```

**Escenario E2 — Estrés checkout completo (350 usuarios, flujo más pesado):**
```bash
python -m locust -f test/locustfile.py --class-picker --headless -u 350 -r 10 --run-time 90s --host http://127.0.0.1:5002 --csv test/resultados/run_E2
```

> Para detener antes del tiempo: `Ctrl+C`

### Escenarios disponibles en locustfile.py

| Clase                 | Escenario            | Wait time  | Usuarios sugeridos |
|-----------------------|----------------------|------------|--------------------|
| `FerremasCargarUser`  | L1 — Carga normal    | 1–3 s      | u=50               |
| `FerremasEstres1User` | E1 — Estrés catálogo | 0.1–0.5 s  | u=200–350          |
| `FerremasEstres2User` | E2 — Estrés checkout | 0.05–0.3 s | u=350              |

### Criterio de quiebre

- **ESTABLE**: error% < 1% **y** p95 < 2000 ms
- **QUIEBRE**: error% >= 1% **o** p95 >= 2000 ms

### Evidencias guardadas en test/resultados/

| Archivo                      |  Escenario |       Resultado                               |
|------------------------------|------------|-----------------------------------------------|
| `run_L1_stats.csv`           | L1 — 50u   | error%=0.000, p95=36ms → **ESTABLE**          |
| `run_E1_stats.csv`           | E1 — 350u  | error%=3.978, p95=2900ms → **QUIEBRE**        |
| `run_E2_stats.csv`           | E2 — 350u  | error%=20.13, p95=6600ms → **QUIEBRE SEVERO** |
| `EVIDENCIA_CARGA_ESTRES.txt` |  **Todos** | Análisis completo con desglose                |

> Error principal en quiebre E1/E2: `WinError 10048` — agotamiento de sockets en Windows.

## Detalle de cada test y cómo ejecutarlo por separado

### test.test_productos — 2 tests unitarios backend
- Qué verifica: funciones del módulo productos (obtener lista y producto por código).
- No requiere ferremas-api (usa SQLite temporal).
- Ejecutar: `python -m unittest test.test_productos`

### test.test_extra — 4 tests unitarios backend
- Qué verifica: listar por categoría, actualizar precio individual, actualizar todos los precios, validar login.
- No requiere ferremas-api (usa SQLite temporal).
- Ejecutar: `python -m unittest test.test_extra`

### test.test_frontend_logica — 4 tests unitarios frontend (FL-001 a FL-004)
- Qué verifica: lógica de negocio de los archivos JavaScript del frontend.
  - FL-001: `mostrarProductos` filtra productos con stock > 10 (solo muestra stock <= 10)
  - FL-002: `mostrarProductos` retorna lista vacía si todos tienen stock > 10
  - FL-003: `mostrarResumenCompra` sin usuario logeado NO aplica descuento
  - FL-004: `mostrarResumenCompra` con usuario logeado aplica 10% de descuento
- No requiere ferremas-api (lógica pura, sin BD ni red).
- Ejecutar: `python -m unittest test.test_frontend_logica`

### test.test_integracion — 10 tests de integración (TI-001 a TI-010)
- Qué verifica:
  - TI-001: `GET /productos` → 200, lista
  - TI-002: `GET /productos/HER001` → 200, datos correctos
  - TI-003: `GET /productos/NOEXIST` → 404
  - TI-004: `GET /api/dolar` (mock) → 200, estructura mindicador
  - TI-005: `POST /webpay/init` (mock) → token_ws + url
  - TI-006: `POST /webpay/commit` (mock) → status AUTHORIZED
  - TI-007: `GET /productos/categoria/Herramientas` → 200, lista con categoría correcta
  - TI-008: `POST /login` → 200, success=True
  - TI-009: `GET /productos/categoria/INVALIDA` → 200, lista vacía
  - TI-010: `POST /registro` → 201, usuario nuevo registrado
- No requiere ferremas-api (usa Flask test_client + mock_server en memoria + SQLite temporal).
- Ejecutar: `python -m unittest test.test_integracion`

### test.test_more — 1 test de integración
- Qué verifica: endpoint `POST /actualizar-precio-usd/HER001` → 200, precio USD esperado.
- No requiere ferremas-api.
- Ejecutar: `python -m unittest test.test_more`

### test.test_criterios_aceptacion — 6 tests (CA-001 a CA-006)
- Qué verifica (reglas de negocio — **NO requiere ferremas-api**):
  - CA-001: todo producto tiene `precio_cl > 0`
  - CA-002: `precio_usd == round(precio_cl / tasa, 2)` (conversión matemáticamente correcta)
  - CA-003: login con contraseña incorrecta → 401
  - CA-004: registro con correo duplicado → 400
  - CA-005: actualizar precios con tasa 0 → 400
  - CA-006: mock de divisa retorna tasa numérica positiva
- Ejecutar: `python -m unittest test.test_criterios_aceptacion`

---

## Mock HTTP para Webpay y Banco Central (mindicador)

Se incluye un mock HTTP en `test/mock_server.py` que simula:
- `GET /api/dolar` → JSON con estructura compatible con mindicador.cl (Banco Central)
- `POST /webpay/init` → crea transacción mock, devuelve `token_ws` y `url` de redirección
- `POST /webpay/commit` → confirma transacción mock, devuelve `status=AUTHORIZED`

**Importante:** el mock_server fue diseñado para uso interno de los tests. Los tests lo usan vía `mock_server.app.test_client()` — sin abrir ningún puerto real. No es un sustituto de ferremas-api para el navegador.

Si necesita levantarlo como proceso independiente para pruebas manuales:

```bash
python test/mock_server.py
```

Por defecto arranca en `http://127.0.0.1:5050`. Variables de entorno disponibles:
- `MOCK_SERVER_PORT` (por defecto 5050)
- `MOCK_SERVER_HOST` (por defecto 127.0.0.1)
- `MOCK_DOLAR_VALOR` (por defecto 950.5)

---

## Nota sobre ferremas-api

Para usar la página web en el navegador sí necesitas ambos servicios:

```bash
# Terminal 1 — backend
cd ferremas-api
venv\Scripts\activate.bat
python app.py          # http://127.0.0.1:5002

# Terminal 2 — frontend
cd ferremas-mvp
venv\Scripts\activate.bat
python app.py          # http://127.0.0.1:5003
```

Luego abrir: `http://127.0.0.1:5003`

---

## Preguntas frecuentes

- **¿Los tests modifican la BD real?** No — usan archivos SQLite temporales que se eliminan en `tearDown()`.
- **¿Los criterios de aceptación necesitan ferremas-api?** No — usan Flask test_client + SQLite temporal + mock en memoria.
- **¿Locust necesita ferremas-api?** Sí — Locust hace llamadas HTTP reales al puerto 5002.
- **¿Puedo correr los 27 tests sin internet?** Sí — no hay llamadas a servicios externos reales.
