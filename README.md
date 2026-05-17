# Ferremas MVP

Sistema MVP de Ferremas desarrollado con arquitectura MVC utilizando Flask y SQLite.

---

# Tecnologías utilizadas

- Python
- Flask
- Flask-CORS
- SQLite
- HTML
- CSS
- JavaScript

---

# Requisitos previos

Instalar previamente en el computador:

## Programas necesarios

- Git
- Python 3.x
- Visual Studio Code (opcional)

---

# Verificar instalación de Python

Abrir PowerShell y ejecutar:

```bash
python --version
```

También verificar pip:

```bash
pip --version
```

Si ambos comandos funcionan correctamente continuar.

---

# Clonar repositorio

Abrir Git Bash o PowerShell en la carpeta deseada y ejecutar:

```bash
git clone URL_DEL_REPOSITORIO
```

Ejemplo:

```bash
git clone https://github.com/usuario/repositorio.git
```

---

# Ingresar al proyecto

```bash
cd "Repo - Ferremas"
```

---

# Abrir proyecto en Visual Studio Code

```bash
code .
```

---

# Crear entorno virtual

Ejecutar:

```bash
python -m venv venv
```

Esto creará la carpeta:

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

# Instalar dependencias del proyecto

Con el entorno virtual activo ejecutar:

```bash
pip install -r requirements.txt
```

Esto instalará automáticamente:
- Flask
- Flask-CORS
- y todas las librerías necesarias.

---

# Crear base de datos SQLite

Ejecutar:

```bash
python MODELO/init_db.py
```

---

# Ejecutar aplicación

```bash
python app.py
```

---

# URL aplicación

Abrir navegador en:

```txt
http://127.0.0.1:5000
```

---

# Actualizar requirements.txt

Cada vez que se instale una nueva librería ejecutar:

```bash
pip freeze > requirements.txt
```

Luego subir cambios a GitHub.

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

Ver archivos modificados:

```bash
git status
```

Agregar cambios:

```bash
git add .
```

Crear commit:

```bash
git commit -m "Descripción cambios"
```

Subir cambios:

```bash
git push
```

---

# Descargar cambios nuevos del repositorio

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

Verificar que Python fue instalado con:

```txt
Add Python to PATH
```

habilitado.

---

# Estructura del proyecto

```txt
Repo - Ferremas/
│
├── MODELO/
│     ├── conexion.py
│     ├── database.sql
│     └── init_db.py
│
├── VISTA/
│     ├── css/
│     ├── js/
│     ├── img/
│     └── templates/
│
├── CONTROLADOR/
│
├── venv/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Funcionalidades actuales

- Visualización productos
- Integración SQLite
- Arquitectura MVC
- Conversión CLP/USD
- Integración API dólar
- Diseño responsive básico

---

# Funcionalidades futuras

- Login usuarios
- Registro usuarios
- Carrito compras
- Integración WebPay
- Sistema descuentos
- Gestión stock
- Panel administrador