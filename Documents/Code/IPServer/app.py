#!/usr/bin/env python3

import socket
import requests
import os
import time

def check_internet():
    try:
        # Try to ping Google DNS server
        response = os.system("ping -c 1 8.8.8.8")
        return response == 0  # If response is 0, ping was successful
    except Exception:
        return False

def get_ip_address():
    # Get the local IP address of the device
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0.1)
    try:
        s.connect(('10.255.255.255', 1))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address

def post_ip_address(ip_address, server_url):
    # Post the IP address to a web server
    data = {'ip_address': ip_address}
    try:
        response = requests.post(server_url, data=data)
        if response.status_code == 200:
            print("IP address posted successfully.")
        else:
            print(f"Failed to post IP address. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error posting IP address: {e}")

if __name__ == "__main__":
    # Replace 'http://your-server.com' with the actual URL where you want to post the IP address
    server_url = 'http://81.0.248.76:5000/post_ip'

    while True:
        # Check if there is internet connectivity
        if check_internet():
            # Get the IP address
            ip_address = get_ip_address()

            # Post the IP address to the server
            post_ip_address(ip_address, server_url)

            # Break out of the loop if successfully posted
            break
        else:
            print("No internet connectivity. Retrying in 5 seconds...")
            time.sleep(5)

