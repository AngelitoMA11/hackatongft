import uuid
import getmac
import psycopg2
from psycopg2 import Error

class UserRegistration:
    def __init__(self, host, database, user, password):
        self.db_params = {
            'host': host,        # Corregido: 'Public-IP' → 'host'
            'database': database,
            'user': user,
            'password': password,
            'port': 5432         # PostgreSQL usa el puerto 5432
        }

    @staticmethod
    def get_mac_address():
        return getmac.get_mac_address()

    def check_user_registration(self):
        connection = None
        try:
            # Obtener la dirección MAC
            mac_address = self.get_mac_address()
            
            # Conectar a PostgreSQL
            connection = psycopg2.connect(**self.db_params)
            cursor = connection.cursor()

            # Verificar si la MAC ya existe en la BD
            cursor.execute("SELECT nombre, apellidos, master FROM usuarios WHERE mac_address = %s", (mac_address,))
            user = cursor.fetchone()

            if user:
                print(f"✅ Usuario registrado: {user[0]} {user[1]} (Master: {user[2]}) - MAC: {mac_address}")
            else:
                print("❌ Usuario no registrado. Por favor, ingrese sus datos:")
                nombre = input("Nombre: ")
                apellidos = input("Apellidos: ")
                master = input("Master: ")

                # Insertar nuevo usuario
                cursor.execute(
                    "INSERT INTO usuarios (nombre, apellidos, master, mac_address) VALUES (%s, %s, %s, %s)",
                    (nombre, apellidos, master, mac_address)
                )
                connection.commit()
                print("✅ Usuario registrado exitosamente!")

        except (Exception, Error) as error:
            print(f"❌ Error conectando a PostgreSQL: {error}")

        finally:
            # Cerrar conexión de forma segura
            if connection:
                cursor.close()
                connection.close()
                print("🔒 Conexión cerrada.")

if __name__ == "__main__":
    registration = UserRegistration('host', 'database', 'username', 'password')
    registration.check_user_registration()