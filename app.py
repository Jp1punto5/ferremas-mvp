from flask import Flask, jsonify, request
from flask_cors import CORS

from modelo.producto_model import (
    obtener_productos,
    obtener_producto,
    listar_productos_categoria
)
from modelo.usuario_model import (
    obtener_usuario_por_correo,
    validar_login,
    registrar_usuario
)
from modelo.utils import formato_producto, respuesta_error, respuesta_exito


app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return respuesta_exito(mensaje="Ferremas MVP funcionando correctamente")


@app.route('/health')
def health():
    return respuesta_exito(data={"status": "online", "app": "Ferremas MVP"})

@app.route('/productos')
def productos():
    try:
        productos = obtener_productos()
        lista_productos = [formato_producto(p) for p in productos]
        return jsonify(lista_productos), 200
    except Exception as e:
        return respuesta_error(f"Error obteniendo productos: {str(e)}", 500)


@app.route('/productos/<codigo_producto>')
def producto_individual(codigo_producto):
    try:
        producto = obtener_producto(codigo_producto)
        if producto:
            return jsonify(formato_producto(producto)), 200
        return respuesta_error("Producto no encontrado", 404)
    except Exception as e:
        return respuesta_error(f"Error: {str(e)}", 500)

# =========================
# OBTENER PRODUCTOS POR CATEGORIA   
# =========================
@app.route('/productos/categoria/<categoria>')
def productos_por_categoria(categoria):
    try:
        productos = listar_productos_categoria(categoria)
        lista_productos = [formato_producto(p) for p in productos]
        return jsonify(lista_productos), 200
    except Exception as e:
        return respuesta_error(f"Error: {str(e)}", 500)




#se crea endpoint de prueba para validar el proceso de login, utilizando un usuario que ya existe en la base de datos.

@app.route(
    '/login',
    methods=['POST']
)
def login():
    try:
        data = request.get_json()
        if not data:
            return respuesta_error("Datos inválidos", 400)
        
        correo = data.get('correo')
        clave = data.get('clave')
        
        if not correo or not clave:
            return respuesta_error("Correo y contraseña requeridos", 400)
        
        usuario = validar_login(correo, clave)
        if usuario:
            return jsonify({
                "success": True,
                "usuario": usuario["nombre_completo"],
                "rol": usuario["rol"]
            }), 200
        
        return respuesta_error("Correo o contraseña incorrectos", 401)
    
    except Exception as e:
        return respuesta_error(f"Error en login: {str(e)}", 500)


# Endpoint para registrar un nuevo usuario, se reciben los datos en formato JSON y se valida que el correo no esté registrado antes de crear el nuevo usuario.

@app.route('/registro', methods=['POST'])
def registro():
    try:
        datos = request.get_json()
        if not datos:
            return respuesta_error("Datos inválidos", 400)
        
        nombre_completo = datos.get('nombre_completo')
        correo = datos.get('correo')
        telefono = datos.get('telefono')
        password = datos.get('password')
        
        if not all([nombre_completo, correo, telefono, password]):
            return respuesta_error("Todos los campos son requeridos", 400)
        
        usuario_existente = obtener_usuario_por_correo(correo)
        if usuario_existente:
            return respuesta_error("El correo ya está registrado", 400)
        
        registrar_usuario(nombre_completo, correo, telefono, password)
        return respuesta_exito(mensaje="Usuario registrado correctamente"), 201
    
    except Exception as e:
        return respuesta_error(f"Error en registro: {str(e)}", 500)






if __name__ == '__main__':
    app.run(debug=True)