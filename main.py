import machine
import neopixel
import urequests
import time
import json
import network

# Wi-Fi configuration
WIFI_SSID = 'Vaibhav 4g'  # Replace with your Wi-Fi SSID
WIFI_PASSWORD = 'rajesh@15'  # Replace with your Wi-Fi password

# Firebase configuration
firebase_url = "https://allprojects68-default-rtdb.asia-southeast1.firebasedatabase.app/vaiLED/selected.json"

n = 210
p = 27

np = neopixel.NeoPixel(machine.Pin(p), n)

# Function to connect to Wi-Fi
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    print(f"Connecting to Wi-Fi network: {ssid}")
    
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(1)
    
    print("\nConnected to Wi-Fi!")
    print("Network Config:", wlan.ifconfig())

# Function to turn off all LEDs
def turn_off_all_leds():
    for i in range(n):
        np[i] = (0, 0, 0)
#     np.write()

# Function to fetch the LED data from Firebase
def fetch_led_data_from_firebase():
    try:
        response = urequests.get(firebase_url)
        if response.status_code == 200:
            print("Data fetched successfully")
            data = response.json()  # Parse the JSON response
            print("Fetched data:", data)  # Debug: Print the fetched data
            return data if data else []  # Ensure it returns an empty list if data is None
        else:
            print("Failed to fetch data. Status code:", response.status_code)
    except Exception as e:
        print("Error fetching data:", e)
    return []

# Function to update LEDs based on the Firebase data
def update_leds(led_indices):
    turn_off_all_leds()  # Turn off all LEDs first
    for i in led_indices:
        if i < n:  # Check to prevent out-of-range indices
            np[i] = (255, 255, 0)
    np.write()

# Main program
def main():
    connect_to_wifi(WIFI_SSID, WIFI_PASSWORD)  # Connect to Wi-Fi

    while True:
        O = fetch_led_data_from_firebase()  # Fetch the selected LEDs from Firebase
        print("Fetched LED indices:", O)
        
        if O:
            update_leds(O)  # Update the LEDs with the fetched data

        time.sleep(10)  # Delay between updates (10 seconds)

# Start the program
if __name__ == "__main__":
    main()

