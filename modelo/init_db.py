import sqlite3

# Crear conexión
conexion = sqlite3.connect('ferremas.db')

# Leer script SQL
with open('MODELO/database.sql', 'r', encoding='utf-8') as archivo_sql:
    script = archivo_sql.read()

# Ejecutar script
conexion.executescript(script)

# Guardar cambios
conexion.commit()

# Cerrar conexión
conexion.close()

print("Base de datos creada correctamente.")