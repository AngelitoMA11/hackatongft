from flask import Flask, request, jsonify, abort
import os
import psycopg2
from dotenv import load_dotenv  

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            mac_address TEXT PRIMARY KEY,
            name TEXT,
            surname TEXT,
            mail TEXT,
            grade TEXT,
            academic_year TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    
app = Flask(__name__)

@app.route("/users/check/<mac_address>", methods=["GET"])
def check_user_registration(mac_address):
    
    conn = get_connection()
    cursor = conn.cursor()
    create_table()
    
    cursor.execute("SELECT * FROM usuarios WHERE mac_address = %s", (mac_address,))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if user:
        return jsonify({"registered": True, "user": user})
    else:
        return jsonify({"registered": False})

@app.route("/users/<mac_address>", methods=["GET"])
def get_user(mac_address):
    conn = get_connection()
    cursor = conn.cursor()
    create_table()
    
    cursor.execute("SELECT * FROM usuarios WHERE mac_address = %s", (mac_address,))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if user:
        return jsonify({"user": {
            "mac_address": user[0],
            "name": user[1],
            "surname": user[2],
            "mail": user[3],
            "grade": user[4],
            "academic_year": user[5]
        }})
    else:
        abort(404, description="Usuario no encontrado")

@app.route("/users/", methods=["POST"])
def create_user():
    data = request.get_json()
    
    if not data or not all(key in data for key in ("mac_address", "name", "surname", "mail", "grade", "academic_year")):
        abort(400, description="Faltan datos requeridos")
    
    mac_address = data["mac_address"]
    name = data["name"]
    surname = data["surname"]
    mail = data["mail"]
    grade = data["grade"]
    academic_year = data["academic_year"]
    
    conn = get_connection()
    cursor = conn.cursor()
    create_table()
    
    cursor.execute("INSERT INTO usuarios (mac_address, name, surname, mail, grade, academic_year) VALUES (%s, %s, %s, %s, %s, %s)",
                   (mac_address, name, surname, mail, grade, academic_year))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Usuario creado exitosamente"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
