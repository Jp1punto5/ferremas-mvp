from flask import Flask, jsonify, request
import time
import os

app = Flask(__name__)


@app.route('/api/dolar', methods=['GET'])
def api_dolar():
    """Simula la respuesta de mindicador.cl para el indicador dólar."""
    value = float(os.environ.get('MOCK_DOLAR_VALOR', '950.5'))
    now = time.strftime('%Y-%m-%dT%H:%M:%S')
    return jsonify({
        "version": "1",
        "autor": "mock",
        "codigo": "dolar",
        "nombre": "Dólar observado",
        "unidad_medida": "Pesos",
        "serie": [
            {
                "fecha": now,
                "valor": value
            }
        ]
    }), 200


@app.route('/webpay/init', methods=['POST'])
def webpay_init():
    """Simula la creación de transacción en Webpay (initTransaction).

    Espera JSON: {buy_order, session_id, amount, return_url}
    Responde con token_ws y url de redirección mock.
    """
    data = request.get_json() or {}
    buy_order = data.get('buy_order', 'MOCK_ORDER')
    token = f"MOCK_TOKEN_{int(time.time())}"
    # URL donde se redirigiría al comprador (mock)
    url = f"https://webpay.mock/redirect?token_ws={token}"
    return jsonify({
        "token_ws": token,
        "token": token,
        "url": url,
        "buy_order": buy_order
    }), 200


@app.route('/webpay/commit', methods=['POST'])
def webpay_commit():
    """Simula la confirmación/commit de la transacción en Webpay.

    Puede recibir form-data con token_ws o JSON {token_ws}
    """
    token = request.form.get('token_ws') or (request.get_json() or {}).get('token_ws')
    if not token:
        return jsonify({"error": "token_ws no recibido"}), 400

    # Extraer información simulada del token
    amount = float(os.environ.get('MOCK_WEBPAY_AMOUNT', '10000'))
    buy_order = os.environ.get('MOCK_WEBPAY_ORDER', 'MOCK_ORDER')

    return jsonify({
        "status": "AUTHORIZED",
        "buy_order": buy_order,
        "amount": amount,
        "response_code": 0,
        "authorization_code": "MOCK_AUTH_1234",
        "token_ws": token
    }), 200


if __name__ == '__main__':
    port = int(os.environ.get('MOCK_SERVER_PORT', '5050'))
    host = os.environ.get('MOCK_SERVER_HOST', '127.0.0.1')
    print(f"Mock server starting on {host}:{port}")
    app.run(host=host, port=port, debug=False)
