from flask import Flask, request, jsonify
import ipaddress
import json
import os
from google.cloud import pubsub_v1
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

PROJECT_ID = os.getenv('GCP_PROJECT_ID')
TOPIC_ID = os.getenv('GCP_TOPIC_ID')

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

@app.route('/datos', methods=['POST'])
def recibir_datos():
    data = request.get_json()
    
    mac_address = data.get('mac_address')
    ip = data.get('ip')
    web = data.get('web')
    timestamp = data.get('timestamp')

    message = {
        'mac_address': mac_address,
        'ip': ip,
        'web': web,
        'timestamp': timestamp
    }

    try:
        future = publisher.publish(topic_path, json.dumps(message).encode("utf-8"))
        print(f"Mensaje publicado: {message}")
    except Exception as e:
        print(f"Error publicando el mensaje: {e}")

    return '', 204 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
