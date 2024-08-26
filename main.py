from machine import ADC , Pin
import neopixel
import urequests
import time
import json
import network

# Wi-Fi configuration
WIFI_SSID = 'Vaibhav 4g'  # Replace with your Wi-Fi SSID
WIFI_PASSWORD = 'rajesh@15'  # Replace with your Wi-Fi password

# Setup ADC for potentiometer
adc = ADC(Pin(35))  # Use GPIO15 for ADC reading (D15)
adc.atten(ADC.ATTN_11DB)  # Configure for full range 0-3.3V
adc.width(ADC.WIDTH_12BIT)  # 12-bit resolution, values 0-4095


# Firebase configuration
firebase_url = "https://allprojects68-default-rtdb.asia-southeast1.firebasedatabase.app/vaiLED/"
led_node = "selected.json"
color_node = "colors.json"

mode = ""

n = 210
p = 27

x, y, z = 0,0,0
brightness = 1

np = neopixel.NeoPixel(Pin(p), n)



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
    data = {"led":[], "color":[]}
    try:
        response = urequests.get(firebase_url + led_node)
        if response.status_code == 200:
            print("Data fetched successfully")
            data["led"] = response.json()  # Parse the JSON response
            print("Fetched led:", data["led"])  # Debug: Print the fetched data
            #return data if data else []  # Ensure it returns an empty list if data is None
        response = urequests.get(firebase_url + color_node)
        if response.status_code == 200:
            print("Data fetched successfully")
            data["color"] = response.json()  # Parse the JSON response
            print("Fetched color:", data["color"])  # Debug: Print the fetched data
        else:
            print("Failed to fetch data. Status code:", response.status_code)
    except Exception as e:
        print("Error fetching data:", e)
    return data["led"], data["color"]

def update_leds(led_indices, led_color):
    global x, y, z, brightness
    turn_off_all_leds()
    
    brightness = adc.read() / 4095
    print(brightness)
    
    for i in led_indices:
        if i < n:
            #np[i] = (led_color["red"], led_color["green"], led_color["blue"])
            np[i] = tuple(int(c * brightness) for c in (led_color["red"], led_color["green"], led_color["blue"]))
            
            
    np.write()

# Function to incrementally update LED colors
def update_leds_rainbow(led_indices):
    global x, y, z
    turn_off_all_leds()  # Turn off all LEDs first

    for i in led_indices:
        if i < n:  # Check to prevent out-of-range indices
            # Create a gradient effect in VIBGYOR color spectrum

            # Cycle through VIBGYOR (Red -> Orange -> Yellow -> Green -> Blue -> Indigo -> Violet)
            if x < 255 and y == 0 and z == 0:
                x += 1  # Increasing Red
            elif x == 255 and z < 255 and y == 0:
                z += 1  # Increasing Blue
            elif z == 255 and x > 0:
                x -= 1  # Decreasing Red
            elif x == 0 and z == 255 and y < 255:
                y += 1  # Increasing Green
            elif y == 255 and z > 0:
                z -= 1  # Decreasing Blue
            elif z == 0 and y > 0:
                y -= 1  # Decreasing Green
            
            # Set the LED color
            np[i] = (x, y, z)

    # Update the LED strip with new colors
    np.write()

# Main program
def main():
    connect_to_wifi(WIFI_SSID, WIFI_PASSWORD)  # Connect to Wi-Fi
    #O = fetch_led_data_from_firebase() 

    while True:
        led_indices, led_color = fetch_led_data_from_firebase()  # Fetch the selected LEDs from Firebase
        #print("Fetched LED indices:", led_indices)
        
        #led_indices = [788, 750, 749, 791, 818, 860, 859, 821, 296, 30, 31, 32, 33, 36, 103, 106, 173, 172, 171, 170, 167, 112, 97, 42, 27, 26, 25, 24, 45, 94, 115, 164, 95, 96, 21, 48, 91, 118, 161, 20, 18, 19, 51, 88, 89, 90, 14, 84, 125, 154, 55, 16, 15, 13, 12, 150, 129, 130, 149]
        
    
        
        if led_indices:
            #update_leds_rainbow(O["led"])  # Update the LEDs with the fetched data
            if mode == "rainbow":
                update_leds_rainbow(led_indices)
            else:
                update_leds(led_indices, led_color)

        time.sleep(5)  # Delay between updates (10 seconds)

# Start the program
if __name__ == "__main__":
    main()
    """while True:
        print(adc.read() / 4095)
        time.sleep(1)"""

