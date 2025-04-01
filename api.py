from flask import Flask, request, jsonify
import ipaddress

app = Flask(__name__)

@app.route('/datos', methods=['POST'])
def recibir_datos():
    data = request.get_json()
    
    nombre = data.get('nombre')
    ip = data.get('ip')

    # Validación básica
    if not nombre or not ip:
        return jsonify({'error': 'Faltan campos requeridos: nombre o ip'}), 400

    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return jsonify({'error': 'IP inválida'}), 400

    print(f"Nombre: {nombre}, IP: {ip}")
    
    return jsonify({'mensaje': 'Datos recibidos correctamente', 'datos': {'nombre': nombre, 'ip': ip}}), 200

if __name__ == '__main__':
    app.run(debug=True)
