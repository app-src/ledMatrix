import network
import socket
from machine import Pin, Timer
import time
import ure

# Wi-Fi configuration
SSID = "SafeHouse"
PASSWORD = "Rg@2k24+-*/"

# Global variable to store the name
stored_name = ""

# Set up Wi-Fi connection
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
    print('Network config:', wlan.ifconfig())

# Read the contents of index.html
def read_index_html():
    with open('index.html', 'r') as file:
        return file.read()

# Save data to a file
def save_data(name):
    with open('stored_data.txt', 'w') as file:
        file.write(name)

# Load data from a file
def load_data():
    try:
        with open('stored_data.txt', 'r') as file:
            return file.read().strip()
    except:
        return ""

# Print stored name every 2 seconds
def print_name(timer):
    global stored_name
    if stored_name:
        print(f"Stored name: {stored_name}")

# Parse the POST request
def parse_post_request(request):
    match = ure.search("name=(.+)", request)
    if match:
        return match.group(1).replace('+', ' ')
    return None

# Main webserver function
def serve_webpage():
    global stored_name
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    
    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024).decode('utf-8')
        
        if request.startswith('POST'):
            name = parse_post_request(request)
            if name:
                stored_name = name
                save_data(stored_name)
                response = "Name saved successfully!"
            else:
                response = "Error: Name not found in request"
        else:
            response = read_index_html()
        
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()

# Main execution
def main():
    global stored_name
    connect_to_wifi()
    stored_name = load_data()
    timer = Timer(-1)
    timer.init(period=2000, mode=Timer.PERIODIC, callback=print_name)
    serve_webpage()

if __name__ == "__main__":
    main()
