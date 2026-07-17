# Ferremas MVP

Sistema MVP de Ferremas desarrollado utilizando arquitectura MVC con Flask.

Este repositorio corresponde al frontend del proyecto, encargado de la interfaz de usuario, renderizado de páginas y la suite de pruebas local. La base de datos SQLite y la lógica de negocio residen en `ferremas-api`.

---

# Arquitectura General

El proyecto Ferremas se encuentra dividido en 2 repositorios independientes. Para ejecutar todas las funcionalidades (UI completa + integraciones) se recomienda ejecutar ambos: `ferremas-api` y `ferremas-mvp`. Sin embargo, la suite de pruebas de `ferremas-mvp` está diseñada para ejecutarse sin levantar `ferremas-api`.

## 1. ferremas-mvp

Repositorio principal del sistema.

Contiene:
- Frontend (HTML, CSS, JavaScript)
- Servidor Flask para servir páginas estáticas
- Arquitectura MVC (vista)
- Carrito de compras
- Flujo de checkout
- Login y registro de usuarios (consume ferremas-api)
- Suite de pruebas (unittest + Locust)

Puerto configurado:

```txt
http://127.0.0.1:5003
```

---

## 2. ferremas-api

Repositorio externo encargado de integraciones, servicios externos y base de datos.

Contiene:
- Base de datos SQLite (schema, seed, modelos)
- Integración Webpay Plus (Transbank QA)
- Conversión de divisas USD/CLP
- Endpoints REST externos

Puerto configurado:

```txt
http://127.0.0.1:5002
```

IMPORTANTE:

Ambos proyectos deben ejecutarse simultáneamente para que todas las funcionalidades funcionen correctamente.

---

# Tecnologías utilizadas

- Python
- Flask
- Flask-CORS
- SQLite
- HTML
- CSS
- JavaScript
- Webpay Plus (Transbank QA)
- API REST

---

# Requisitos previos

Instalar previamente en el computador:

- Git
- Python 3.x
- Visual Studio Code (opcional)

---

# Verificar instalación de Python

Abrir PowerShell o CMD y ejecutar:

```bash
python --version
```

Verificar también pip:

```bash
pip --version
```

---

# Clonar repositorios

## Clonar ferremas-api

```bash
git clone https://github.com/Jp1punto5/ferremas-api
```

---

## Clonar ferremas-mvp

```bash
git clone https://github.com/Jp1punto5/ferremas-mvp
```

---

# Estructura esperada

Se recomienda mantener ambos repositorios dentro de una misma carpeta:

```txt
Proyecto Ferremas/
│
├── ferremas-api/
│
└── ferremas-mvp/
```

---

# Configuración de ferremas-api

IMPORTANTE:

Para ejecutar la aplicación completa (UI + API) levantar primero `ferremas-api` y luego `ferremas-mvp`. Si solo desea ejecutar la suite de pruebas de `ferremas-mvp`, no es necesario levantar `ferremas-api`.

---

## Ingresar al proyecto

```bash
cd ferremas-api
```

---

## Abrir en Visual Studio Code

```bash
code .
```

---

## Crear entorno virtual

```bash
python -m venv venv
```

---

## Activar entorno virtual

### PowerShell

```bash
.\venv\Scripts\Activate.ps1
```

### CMD

```bash
venv\Scripts\activate.bat
```

---

## Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

---

## Crear base de datos SQLite

Este paso solo se realiza la primera vez (o si se borra la BD):

```bash
python modelo/init_db.py
```

Esto genera automáticamente:
- Base de datos SQLite (`ferremas.db`)
- Tablas del schema
- Datos de prueba (productos y usuarios iniciales)

---

## Ejecutar API

```bash
python app.py
```

---

## Verificar ejecución

Abrir navegador en:

```txt
http://127.0.0.1:5002
```

Se espera visualizar un mensaje indicando que la API se encuentra funcionando correctamente.

Si la API se encuentra levantada correctamente se podrán utilizar:
- Base de datos (productos, usuarios)
- Conversión USD/CLP
- Integración Webpay
- Confirmación de pagos

---

## Ingresar al proyecto

```bash
cd ferremas-mvp
```

---

# Abrir en Visual Studio Code

```bash
code .
```

---

# Crear entorno virtual

```bash
python -m venv venv
```

Esto creará automáticamente la carpeta:

```txt
venv/
```

---

# Activar entorno virtual

## PowerShell

```bash
.\venv\Scripts\Activate.ps1
```

## CMD

```bash
venv\Scripts\activate.bat
```

Si el entorno virtual se activó correctamente aparecerá:

```txt
(venv)
```

al inicio de la terminal.

---

# Instalar dependencias

Con el entorno virtual activo ejecutar:

```bash
python -m pip install -r requirements.txt
```

Esto instalará automáticamente todas las librerías necesarias del proyecto.

Nota (Windows/venv): si `pip` falla por launcher, usar siempre `python -m pip ...`.

---

# Ejecutar aplicación

```bash
python app.py
```

---

# URL aplicación

Abrir navegador en:

```txt
http://127.0.0.1:5003/vista/catalogo_p.html
```

Si el proyecto se encuentra funcionando correctamente se visualizará el catálogo principal del sistema.

---

# Orden correcto de ejecución

IMPORTANTE:

El orden correcto para ejecutar el sistema es:

## 1. Levantar ferremas-api

```txt
Puerto 5002
```

IMPORTANTE:

Si se modifica el puerto será necesario actualizar los `fetch()` y endpoints utilizados por el frontend.

---

## 2. Levantar ferremas-mvp

```txt
Puerto 5003
```

IMPORTANTE:

Si se modifica el puerto será necesario actualizar las rutas correspondientes del proyecto.

---

## 3. Abrir aplicación

```txt
http://127.0.0.1:5003/vista/catalogo_p.html
```

---

# Pruebas (unitarias, integración, carga y estrés)

Para ejecución de pruebas y comandos oficiales de Locust en la terminal integrada de VS Code, revisar:

```txt
ferremas-mvp/test/README.md
```

Ahí se documenta el paso a paso para:
- Ejecutar `python -m unittest discover -v`
- Ejecutar Locust con barrido incremental de concurrencia y detectar el límite real de quiebre.

---

# Tarjetas de prueba Webpay Plus (QA)

El proyecto utiliza el entorno de pruebas QA de Transbank Webpay Plus.

Estas tarjetas permiten simular pagos aprobados y rechazados durante las pruebas del sistema.

---

## Pago aprobado

```txt
Número tarjeta: 4051885600446623
CVV: 123
Fecha expiración: Cualquier fecha futura
RUT: 11.111.111-1
Clave: 123
Resultado esperado: TRANSACCIÓN APROBADA
```

---

## Pago rechazado

```txt
Número tarjeta: 4051885600446607
CVV: 123
Fecha expiración: Cualquier fecha futura
RUT: 11.111.111-1
Clave: 123
Resultado esperado: TRANSACCIÓN RECHAZADA
```

---

# Funcionalidades actuales

- Arquitectura MVC (vista)
- Visualización de productos (consume ferremas-api)
- Login de usuarios (consume ferremas-api)
- Registro de usuarios (consume ferremas-api)
- Carrito de compras
- Flujo de checkout
- Conversión USD/CLP (consume ferremas-api)
- Integración Webpay Plus (consume ferremas-api)
- Confirmación de pagos
- Persistencia temporal mediante SessionStorage
- Identificación de usuario activo
- Sistema de descuentos por login
- Diseño responsive básico
- Suite de 13 tests unitarios e integración (sin levantar ferremas-api)

---

# Estructura del proyecto

```txt
ferremas-mvp/
│
├── modelo/  ← Scaffolding de pruebas (shims para tests unitarios/integración)
│     ├── conexion.py        (shim: en producción lanza RuntimeError; los tests lo parchean)
│     ├── producto_model.py  (funciones de productos usadas por app.py y tests)
│     ├── usuario_model.py   (funciones de usuarios usadas por app.py y tests)
│     └── utils.py           (formateo de respuestas)
│
│   NOTA: la versión canónica del modelo (BD real) está en ferremas-api/modelo/
│
├── test/
│     ├── __init__.py
│     ├── test_setup.py          (crea DB SQLite temporal para tests)
│     ├── test_productos.py      (tests unitarios de productos)
│     ├── test_extra.py          (tests unitarios extras)
│     ├── test_integracion.py    (tests de integración + mocks Webpay/divisa)
│     ├── test_more.py           (tests adicionales de integración)
│     ├── mock_server.py         (mock de Webpay y banco central/mindicador)
│     ├── locustfile.py          (escenario Locust para carga y estrés)
│     ├── resultados/            (CSVs y evidencias de Locust)
│     ├── README.md              (guía de tests)
│     ├── DESCRIPCION_TESTS.md   (detalle de cada test)
│     └── TESTS_REPORT.md        (reporte de resultados)
│
├── vista/
│     ├── css/
│     ├── js/
│     ├── img/
│     ├── catalogo_p.html
│     └── ...
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Actualizar requirements.txt

Cada vez que se instale una nueva librería ejecutar:

```bash
python -m pip freeze > requirements.txt
```

Luego subir los cambios al repositorio.

---

# Instalar nueva librería

Ejemplo:

```bash
python -m pip install flask-cors
```

Actualizar requirements:

```bash
python -m pip freeze > requirements.txt
```

---

# Subir cambios a GitHub

IMPORTANTE:

Los siguientes comandos solo deben utilizarse si se tiene acceso para subir cambios al repositorio.

---

## Ver archivos modificados

```bash
git status
```

---

## Agregar cambios

```bash
git add .
```

---

## Crear commit

```bash
git commit -m "Descripción cambios"
```

---

## Subir cambios

```bash
git push
```

---

# Descargar cambios del repositorio

```bash
git pull
```

---

# Problemas comunes

## Error: flask_cors no encontrado

Instalar:

```bash
python -m pip install flask-cors
```

---

## Error: No module named flask

Instalar:

```bash
python -m pip install flask
```

---

## Error: python no reconocido

Verificar que Python fue instalado con la opción:

```txt
Add Python to PATH
```

habilitada.

---

# Notas importantes

- No subir la carpeta `venv/`
- No subir archivos `.db`
- Mantener actualizado `requirements.txt` con `python -m pip freeze > requirements.txt`
- Ejecutar primero `ferremas-api` (puerto 5002), luego `ferremas-mvp` (puerto 5003)
- Verificar que ambos puertos estén disponibles
- La base de datos se inicializa SOLO en `ferremas-api` con `python modelo/init_db.py`
- Para ejecutar los tests NO es necesario levantar `ferremas-api` (usan mock y BD temporal)
- Si `pip` falla por launcher en Windows, siempre usar `python -m pip ...`

---