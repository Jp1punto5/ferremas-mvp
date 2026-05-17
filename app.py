from flask import Flask, jsonify, request
from flask_cors import CORS

from modelo.producto_model import (
    obtener_productos,
    obtener_producto
)
from modelo.usuario_model import (
    obtener_usuario_por_correo,
    validar_login,
    registrar_usuario
)


app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return jsonify({
        "mensaje": "Ferremas MVP funcionando correctamente"
    })


@app.route('/health')
def health():
    return jsonify({
        "status": "online",
        "app": "Ferremas MVP"
    })

@app.route('/productos')
def productos():

    productos = obtener_productos()

    lista_productos = []

    for producto in productos:

        lista_productos.append({
            "codigo_producto": producto["codigo_producto"],
            "nombre": producto["nombre"],
            "descripcion": producto["descripcion"],
            "precio": producto["precio"],
            "stock": producto["stock"],
            "url_foto": producto["url_foto"],
            "categoria": producto["categoria"]
        })

    return jsonify(lista_productos)


@app.route('/productos/<codigo_producto>')
def producto_individual(codigo_producto):

    producto = obtener_producto(codigo_producto)

    if producto:

        return jsonify({
            "codigo_producto": producto["codigo_producto"],
            "nombre": producto["nombre"],
            "descripcion": producto["descripcion"],
            "precio": producto["precio"],
            "stock": producto["stock"],
            "url_foto": producto["url_foto"],
            "categoria": producto["categoria"]
        })

    return jsonify({
        "error": "Producto no encontrado"
    }), 404


#se crea endpoint de prueba para validar el proceso de login, utilizando un usuario que ya existe en la base de datos.

@app.route('/test-login')
def test_login():

    usuario = validar_login(
        'cliente@ferremas.cl',
        '123456'
    )

    if usuario:

        return jsonify({
            "success": True,
            "usuario": usuario["nombre_completo"],
            "rol": usuario["rol"]
        })

    return jsonify({
        "success": False
    })


# Endpoint para registrar un nuevo usuario, se reciben los datos en formato JSON y se valida que el correo no esté registrado antes de crear el nuevo usuario.

@app.route('/registro', methods=['POST'])
def registro():

    datos = request.get_json()

    nombre_completo = datos.get('nombre_completo')
    correo = datos.get('correo')
    telefono = datos.get('telefono')
    password = datos.get('password')

    # =========================
    # VALIDAR USUARIO EXISTENTE
    # =========================

    usuario_existente = obtener_usuario_por_correo(correo)

    if usuario_existente:

        return jsonify({
            "success": False,
            "mensaje": "El correo ya está registrado"
        }), 400

    # =========================
    # REGISTRAR USUARIO
    # =========================

    registrar_usuario(
        nombre_completo,
        correo,
        telefono,
        password
    )

    return jsonify({
        "success": True,
        "mensaje": "Usuario registrado correctamente"
    })











if __name__ == '__main__':
    app.run(debug=True)

