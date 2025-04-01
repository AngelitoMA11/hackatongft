import urllib.request
import json
import ssl

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
