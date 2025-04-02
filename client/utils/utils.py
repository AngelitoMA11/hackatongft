import getmac
import urllib.request
import json
import ssl
import requests
import os
from mitmproxy import http



def get_mac_address():
    return getmac.get_mac_address()

def get_public_ip():
    try:
        context = ssl._create_unverified_context()
        response = urllib.request.urlopen('https://api.ipify.org?format=json', context=context)
        data = response.read().decode('utf-8')
        ip = json.loads(data)['ip']
        return ip
    except Exception as e:
        print(f"First method failed: {e}")
    return "Could not determine public IP"

url_storage = []  # Global list to store URLs

def get_web(flow: http.HTTPFlow):
    try:
        if flow.request.pretty_url:
            url = flow.request.pretty_url
            url_storage.append(url)  # Store URL in the list
            return url
        return "No URL found"
    except Exception as e:
        print(f"Error getting web URL: {e}")
        return "Could not determine web URL"

def is_mac_registered(mac_address):
    try:
        service_url = os.environ.get('CLOUD_RUN_SERVICE_URL')
        
        if not service_url:
            print("Error: CLOUD_RUN_SERVICE_URL environment variable not set")
            return False
        
        response = requests.get(f"{service_url}/users/check/{mac_address}")
        
        if response.status_code == 200:
            data = response.json()
            return data.get('registered')
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            return False
    except Exception as e:
        print(f"Error checking MAC registration: {str(e)}")
        return False

def insert_user_data(mac_address, name, surname, email, grade, academic_year):
    try:
        service_url = os.environ.get('CLOUD_RUN_SERVICE_URL')
        
        if not service_url:
            print("Error: CLOUD_RUN_SERVICE_URL environment variable not set")
            return False
        
        data = {
            "mac_address": mac_address,
            "name": name,
            "surname": surname,
            "mail": email,
            "grade": grade,
            "academic_year": academic_year
        }
        
        response = requests.post(f"{service_url}/users/", json=data)
        
        if response.status_code == 201:
            print("User data inserted successfully.")
            return True
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            return False
    except Exception as e:
        print(f"Error inserting user data: {str(e)}")
        return False
    
def send_data_to_endpoint(data):
    try:
        service_url = os.environ.get('CLOUD_RUN_SERVICE_URL')
        
        if not service_url:
            print("Error: CLOUD_RUN_SERVICE_URL environment variable not set")
            return False
        
        response = requests.post(f"{service_url}/data/", json=data)
        
        if response.status_code == 200:
            print("Data sent successfully.")
            return True
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            return False
    except Exception as e:
        print(f"Error sending data: {str(e)}")
        return False