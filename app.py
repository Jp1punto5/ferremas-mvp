from flask import Flask, jsonify

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)