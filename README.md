# Ferremas MVP

MVP del sistema Ferremas desarrollado con arquitectura MVC utilizando Flask y SQLite.

---

# Tecnologías utilizadas

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript

---

# Arquitectura

El proyecto utiliza arquitectura MVC:

- MODELO
- VISTA
- CONTROLADOR

---

# Crear entorno virtual

```bash
python -m venv venv
```

---

# Activar entorno virtual

## PowerShell

```bash
.\venv\Scripts\Activate.ps1
```

---

# Instalar Flask

```bash
pip install flask
```

---

# Generar archivo requirements.txt

```bash
pip freeze > requirements.txt
```

---

# Instalar dependencias desde requirements.txt

```bash
pip install -r requirements.txt
```

---

# Crear base de datos SQLite

```bash
python MODELO/init_db.py
```

---

# Ejecutar aplicación

```bash
python app.py
```

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

# Actualizar requirements.txt

Cada vez que se instale una nueva librería ejecutar:

```bash
pip freeze > requirements.txt


# Funcionalidades futuras

- Login usuarios
- Registro usuarios
- Catálogo productos
- Carrito compras
- Integración WebPay
- Integración API dólar
- Sistema descuentos