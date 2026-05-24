from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
import os

from modelo.producto_model import (
    obtener_productos,
    obtener_producto,
    listar_productos_categoria,
    actualizar_precio_usd,
    actualizar_todos_precios_usd
)
from modelo.usuario_model import (
    obtener_usuario_por_correo,
    validar_login,
    registrar_usuario
)
from modelo.utils import formato_producto, respuesta_error, respuesta_exito


app = Flask(__name__, static_folder='vista', static_url_path='/vista')
CORS(app)

# Configurar carpeta de archivos estáticos
vista_path = os.path.join(os.path.dirname(__file__), 'vista')


@app.route('/')
def home():
    return respuesta_exito(mensaje="Ferremas MVP funcionando correctamente")


@app.route('/health')
def health():
    return respuesta_exito(data={"status": "online", "app": "Ferremas MVP"})


# ========================================
# SERVIR ARCHIVOS HTML
# ========================================

@app.route('/vista/carrito.html')
def carrito_page():
    """Servir página de carrito"""
    try:
        return send_file(os.path.join(vista_path, 'carrito.html'), mimetype='text/html')
    except Exception as e:
        return respuesta_error(f"Página no encontrada: {str(e)}", 404)


@app.route('/vista/catalogo_p.html')
def catalogo_page():
    """Servir página de catálogo"""
    try:
        return send_file(os.path.join(vista_path, 'catalogo_p.html'), mimetype='text/html')
    except Exception as e:
        return respuesta_error(f"Página no encontrada: {str(e)}", 404)


@app.route('/vista/categoria_p.html')
def categoria_page():
    """Servir página de categoría"""
    try:
        return send_file(os.path.join(vista_path, 'categoria_p.html'), mimetype='text/html')
    except Exception as e:
        return respuesta_error(f"Página no encontrada: {str(e)}", 404)


@app.route('/vista/pago-confirmado.html')
def pago_confirmado_page():
    """Página de confirmación de pago"""
    try:
        return send_file(os.path.join(vista_path, 'pago-confirmado.html'), mimetype='text/html')
    except Exception as e:
        return respuesta_error(f"Página no encontrada: {str(e)}", 404)


@app.route('/pago-confirmado')
def pago_confirmado():
    """Ruta alternativa para confirmación de pago"""
    try:
        return send_file(os.path.join(vista_path, 'pago-confirmado.html'), mimetype='text/html')
    except Exception as e:
        return respuesta_error(f"Página no encontrada: {str(e)}", 404)


# Servir archivos estáticos usando send_from_directory
@app.route('/vista/js/<path:filename>')
def serve_js(filename):
    """Servir archivos JavaScript"""
    return send_from_directory(os.path.join(vista_path, 'js'), filename)


@app.route('/vista/css/<path:filename>')
def serve_css(filename):
    """Servir archivos CSS"""
    return send_from_directory(os.path.join(vista_path, 'css'), filename)


@app.route('/vista/img/<path:filename>')
def serve_img(filename):
    """Servir imágenes"""
    return send_from_directory(os.path.join(vista_path, 'img'), filename)


# Favicon - Comentado: archivo no existe en vista/
# Si deseas usar favicon, coloca favicon.ico en la carpeta vista/
# @app.route('/favicon.ico')
# def favicon():
#     """Servir favicon"""
#     return send_from_directory(vista_path, 'favicon.ico', mimetype='image/x-icon')


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
        return jsonify({

            "success":True,
            "mensaje":
                "Usuario registrado correctamente"

        }), 201
    
    except Exception as e:
        return respuesta_error(f"Error en registro: {str(e)}", 500)


# =========================
# ACTUALIZAR PRECIOS USD
# =========================

@app.route('/actualizar-precios-usd', methods=['POST'])
def actualizar_precios_endpoint():
    """
    Endpoint para actualizar todos los precios USD basados en tasa de cambio.
    
    Body esperado:
    {
        "tasa_cambio": 950.5
    }
    """
    try:
        data = request.get_json()
        if not data:
            return respuesta_error("Datos inválidos", 400)
        
        tasa_cambio = data.get('tasa_cambio')
        if not tasa_cambio or tasa_cambio <= 0:
            return respuesta_error("Tasa de cambio inválida", 400)
        
        resultado = actualizar_todos_precios_usd(tasa_cambio)
        return jsonify(resultado), 200 if resultado['success'] else 500
    
    except Exception as e:
        return respuesta_error(f"Error al actualizar precios: {str(e)}", 500)


@app.route('/actualizar-precio-usd/<codigo_producto>', methods=['POST'])
def actualizar_precio_individual(codigo_producto):
    """
    Endpoint para actualizar precio USD de un producto específico.
    
    Body esperado:
    {
        "tasa_cambio": 950.5
    }
    """
    try:
        data = request.get_json()
        if not data:
            return respuesta_error("Datos inválidos", 400)
        
        tasa_cambio = data.get('tasa_cambio')
        if not tasa_cambio or tasa_cambio <= 0:
            return respuesta_error("Tasa de cambio inválida", 400)
        
        exito = actualizar_precio_usd(codigo_producto, tasa_cambio)
        if exito:
            producto = obtener_producto(codigo_producto)
            if producto:
                return jsonify({
                    "success": True,
                    "mensaje": "Precio USD actualizado",
                    "producto": formato_producto(producto)
                }), 200
            return respuesta_error("Producto no encontrado después de actualizar", 404)
        
        return respuesta_error("No se pudo actualizar el precio", 500)
    
    except Exception as e:
        return respuesta_error(f"Error: {str(e)}", 500)




if __name__ == '__main__':
    app.run(debug=True, port=5003)