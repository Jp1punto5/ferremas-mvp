import sqlite3

# Crear conexión
conexion = sqlite3.connect('ferremas.db')

# =========================
# CREAR TABLAS
# =========================

with open('MODELO/database.sql', 'r', encoding='utf-8') as archivo_sql:
    script_db = archivo_sql.read()

conexion.executescript(script_db)

print("Tablas creadas correctamente.")

# =========================
# INSERTAR DATOS INICIALES
# =========================

with open('MODELO/seed_data.sql', 'r', encoding='utf-8') as archivo_seed:
    script_seed = archivo_seed.read()

conexion.executescript(script_seed)

print("Datos iniciales insertados correctamente.")

# Guardar cambios
conexion.commit()

# Cerrar conexión
conexion.close()

print("Base de datos inicializada correctamente.")