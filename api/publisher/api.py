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
    nombre = data.get('nombre')
    ip = data.get('ip')

    if not nombre or not ip:
        return jsonify({'error': 'Faltan campos: nombre o ip'}), 400

    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return jsonify({'error': 'IP inválida'}), 400

    mensaje = {'nombre': nombre, 'ip': ip}
    try:
        mensaje_json = json.dumps(mensaje)
        publisher.publish(topic_path, mensaje_json.encode('utf-8'))
        return jsonify({'mensaje': 'Publicado correctamente', 'datos': mensaje}), 200
    except Exception as e:
        return jsonify({'error': 'Fallo al publicar', 'detalle': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
