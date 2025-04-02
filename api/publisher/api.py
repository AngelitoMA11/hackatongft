from flask import Flask, request, jsonify
import ipaddress
import json
import os
from google.cloud import pubsub_v1
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

PROJECT_ID = os.getenv('GCP_PROJECT_ID')
TOPIC_ID = os.getenv('GCP_TOPIC_ID')

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

@app.route('/datos', methods=['POST'])
def recibir_datos():
    data = request.get_json()

    # Datos desde la rama Final-terraform
    nombre = data.get('nombre')

    # Datos desde la rama main
    mac_address = data.get('mac_address')
    ip = data.get('ip')
    web = data.get('web')
    timestamp = data.get('timestamp')

    # Validación de campos
    if not nombre or not ip:
        return jsonify({'error': 'Faltan campos: nombre o ip'}), 400

    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return jsonify({'error': 'IP inválida'}), 400

    # Construir el mensaje combinando ambas ramas
    mensaje = {
        'nombre': nombre,
        'mac_address': mac_address,
        'ip': ip,
        'web': web,
        'timestamp': timestamp
    }

    try:
        mensaje_json = json.dumps(mensaje)
        publisher.publish(topic_path, mensaje_json.encode('utf-8'))
        print(f"Mensaje publicado: {mensaje}")
        return jsonify({'mensaje': 'Publicado correctamente', 'datos': mensaje}), 200
    except Exception as e:
        print(f"Error publicando el mensaje: {e}")
        return jsonify({'error': 'Fallo al publicar', 'detalle': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
