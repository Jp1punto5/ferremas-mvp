# Ferremas MVP

Sistema MVP de Ferremas desarrollado utilizando arquitectura MVC con Flask y SQLite.

Este repositorio corresponde al sistema principal del proyecto, encargado del frontend, lógica interna, autenticación de usuarios y base de datos local.

---

# Arquitectura General

El proyecto Ferremas se encuentra dividido en 2 repositorios independientes que deben ejecutarse simultáneamente.

## 1. ferremas-mvp

Repositorio principal del sistema.

Contiene:
- Frontend
- Backend interno
- Arquitectura MVC
- Base de datos SQLite
- Carrito de compras
- Flujo de checkout
- Consumo de APIs externas
- Login de usuarios
- Registro de usuarios

Puerto configurado:

```txt
http://127.0.0.1:5003
```

---

## 2. ferremas-api

Repositorio externo encargado de integraciones y servicios externos.

Contiene:
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

El repositorio `ferremas-api` debe levantarse primero.

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
pip install -r requirements.txt
```

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
- Conversión USD/CLP
- Integración Webpay
- Confirmación de pagos

---

# Configuración de ferremas-mvp

Una vez levantada la API externa continuar con este repositorio.

---

# Ingresar al proyecto

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
pip install -r requirements.txt
```

Esto instalará automáticamente todas las librerías necesarias del proyecto.

---

# Crear base de datos SQLite

Ejecutar:

```bash
python modelo/init_db.py
```

Esto generará automáticamente:
- Base de datos SQLite
- Usuarios iniciales
- Productos de prueba para el MVP

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

- Arquitectura MVC
- Base de datos SQLite
- Visualización de productos
- Login de usuarios
- Registro de usuarios
- Carrito de compras
- Flujo de checkout
- Conversión USD/CLP
- Integración API externa
- Integración Webpay Plus
- Confirmación de pagos
- Persistencia temporal mediante SessionStorage
- Identificación de usuario activo
- Sistema de descuentos por login
- Diseño responsive básico

---

# Estructura del proyecto

```txt
ferremas-mvp/
│
├── modelo/
│     ├── conexion.py
│     ├── database.sql
│     ├── init_db.py
│     ├── producto_model.py
│     ├── seed_data.py
│     ├── usuario_model.py
│     └── utils.py
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
pip freeze > requirements.txt
```

Luego subir los cambios al repositorio.

---

# Instalar nueva librería

Ejemplo:

```bash
pip install flask-cors
```

Actualizar requirements:

```bash
pip freeze > requirements.txt
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
pip install flask-cors
```

---

## Error: No module named flask

Instalar:

```bash
pip install flask
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
- Mantener actualizado `requirements.txt`
- Ejecutar primero `ferremas-api`
- Verificar que ambos puertos estén disponibles

---