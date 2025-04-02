import time
import json
from utils.utils import get_mac_address, get_public_ip, is_mac_registered, insert_user_data, send_data_to_endpoint
from dotenv import load_dotenv

load_dotenv()

def main():
    mac_address = get_mac_address()
    
    if not is_mac_registered(mac_address):
        name = input("Enter your name: ")
        surname = input("Enter your surname: ")
        email = input("Enter your email: ")
        grade = input("Enter your grade: ")
        academic_year = input("Enter your academic year: ")
        insert_user_data(mac_address, name, surname, email, grade, academic_year)
        
    while True:
        ip_address = get_public_ip()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        data_to_send = {
            "mac_address": mac_address,
            "public_ip": ip_address,
            "timestamp": timestamp
        }
        
        send_data_to_endpoint(data_to_send)
        time.sleep(15)

if __name__ == "__main__":
    main()