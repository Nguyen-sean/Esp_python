import network
import socket
import time
import machine
from wifi_config import WIFI_SSID, WIFI_PASSWORD
from data_config import LOCATION
from effects import standby  # Import the standby effect module

def write_config(ssid, password):
    try:
        with open('wifi_config.py', 'w') as f:
            f.write(f'WIFI_SSID = "{ssid}"\n')
            f.write(f'WIFI_PASSWORD = "{password}"\n')
    except Exception as e:
        print("Error writing config:", e)

def create_access_point():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="ESP32_Setup", authmode=network.AUTH_WPA_WPA2_PSK, password="12345678")
    print("Access point created with SSID: ESP32_Setup, Password: 12345678")
    return ap

# Load HTML content from a separate file
html = ""
with open("status.html", "r") as f:
    html = f.read()

def start_web_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Web server started on http://192.168.4.1")

    while True:
        cl, addr = s.accept()
        print('Client connected from', addr)
        request = cl.recv(1024)
        request = request.decode('utf-8')

        if 'POST /submit' in request:
            body_start = request.find("\r\n\r\n") + 4
            body = request[body_start:]
            params = {key: value for (key, value) in (item.split('=') for item in body.split('&'))}
            ssid = params.get('ssid', '')
            password = params.get('password', '')

            # Save credentials and restart
            write_config(ssid, password)
            print("Config file written")
            cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
            cl.send('<h1>Credentials Saved. Restarting...</h1>')
            cl.close()
            time.sleep(3)
            machine.reset()

        else:
            # Substitute placeholders in the HTML file
            wifi_status = "Connected" if network.WLAN(network.STA_IF).isconnected() else "Disconnected"
            thingspeak_status = "Connected" if check_thingspeak_connection() else "Disconnected"
            
            response_html = html.replace("{{LOCATION}}", LOCATION)
            response_html = response_html.replace("{{WIFI_STATUS}}", wifi_status)
            response_html = response_html.replace("{{THINGSPEAK_STATUS}}", thingspeak_status)

            cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
            cl.send(response_html)
            cl.close()

def check_thingspeak_connection():
    # Function to check if ThingSpeak connection is successful
    # For now, just return True/False for demonstration purposes
    # You can add your actual code here to check the connection
    return True

def connect():
    if not WIFI_SSID or not WIFI_PASSWORD:
        print("No Wi-Fi credentials saved in config.")
        ap = create_access_point()
        start_web_server()
        return False

    station = network.WLAN(network.STA_IF)
    station.active(True)

    max_retries = 3
    retries = 0

    try:
        while retries < max_retries:
            print(f'Connecting to WiFi... (Attempt {retries + 1}/{max_retries})')
            station.connect(WIFI_SSID, WIFI_PASSWORD)
            timeout = 15  # Set a short timeout for connection attempt
            start_time = time.time()

            while not station.isconnected():
                if time.time() - start_time > timeout:
                    print("Connection attempt timed out. Retrying...")
                    retries += 1
                    station.disconnect()
                    break  # Exit inner while loop to retry connection
                standby(0.03)  # Optional: Run a standby effect
                print("Waiting for connection...")

            if station.isconnected():
                print('Connected to WiFi, network config:', station.ifconfig())
                # Host the additional web page when connected
                start_web_server()
                return True

        print("Max retries reached. Could not connect to WiFi.")
        return False

    except Exception as e:
        print("An error occurred:", e)
        return False
