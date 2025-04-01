import time
import json
from mac_checker import get_mac_address
from network_info import get_public_ip
from database import insert_user_data, get_user_data
from api_client import send_data_to_endpoint

def main():
    mac_address = get_mac_address()
    
    if not is_mac_registered(mac_address):
        name = input("Enter your name: ")
        surname = input("Enter your surname: ")
        email = input("Enter your email: ")
        grade = input("Enter your grade: ")
        academic_year = input("Enter your academic year: ")
        insert_user_data(mac_address, name, surname, email, grade, academic_year)
    
    user_data = get_user_data(mac_address)
    
    while True:
        ip_address = get_public_ip()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        data_to_send = {
            "mac_address": user_data.mac_address,
            "name": user_data.name,
            "surname": user_data.surname,
            "email": user_data.email,
            "grade": user_data.grade,
            "academic_year": user_data.academic_year,
            "public_ip": ip_address,
            "timestamp": timestamp
        }
        
        send_data_to_endpoint(data_to_send)
        time.sleep(30)

if __name__ == "__main__":
    main()