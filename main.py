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
led_indices, led_color = [], []

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
    global led_indices, led_color
    #data = {"led":[], "color":[]}
    try:
        response = urequests.get(firebase_url + led_node)
        if response.status_code == 200:
            print("Data fetched successfully")
            led_indices = response.json()  # Parse the JSON response
            print("Fetched led:", led_indices)  # Debug: Print the fetched data
            #return data if data else []  # Ensure it returns an empty list if data is None
        response = urequests.get(firebase_url + color_node)
        if response.status_code == 200:
            print("Data fetched successfully")
            led_color = response.json()  # Parse the JSON response
            print("Fetched color:", led_color)  # Debug: Print the fetched data
        else:
            print("Failed to fetch data. Status code:", response.status_code)
    except Exception as e:
        print("Error fetching data:", e)
    #return data["led"], data["color"]

# Function to fetch the LED data from Firebase
def fetch_img_data_from_firebase():
    global led_indices
    #data = {"led":[], "color":[]}
    try:
        response = urequests.get(firebase_url + "img.json")
        if response.status_code == 200:
            print("Data fetched successfully")
            led_indices = response.json()  # Parse the JSON response
            print("Fetched led:", led_indices)  # Debug: Print the fetched data
            #return data if data else []  # Ensure it returns an empty list if data is None
    except Exception as e:
        print("Error fetching data:", e)

def update_leds():
    global led_indices, led_color
    turn_off_all_leds()
    
    brightness = adc.read() / 4095
    #print(brightness)
    
    for i in led_indices:
        if i < n:
            #np[i] = (led_color["red"], led_color["green"], led_color["blue"])
            np[i] = tuple(int(c * brightness) for c in (led_color["red"], led_color["green"], led_color["blue"]))
            
            
    np.write()
    
def update_leds_img():
    global led_indices
    turn_off_all_leds()
    
    brightness = adc.read() / 4095
    #print(brightness)
    #print(led_indices)
    
    for i in range(n):
        if True:
            #np[i] = (led_color["red"], led_color["green"], led_color["blue"])
            np[i] = tuple(int(c * brightness) for c in (led_indices[i][0], led_indices[i][1], led_indices[i][2]))
            #print(led_indices[i][0], led_indices[i][1], led_indices[i][2])
            
            
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

# Main program
def main2():
    last_fetch_time = time.time()  # Record the start time
    connect_to_wifi(WIFI_SSID, WIFI_PASSWORD)  # Connect to Wi-Fi
    
    fetch_led_data_from_firebase()  # Initial fetch

    while True:
        current_time = time.time()  # Get the current time
        
        # Check if 5 seconds have elapsed since the last fetch
        if current_time - last_fetch_time >= 200:
            fetch_led_data_from_firebase()  # Fetch new data
            update_leds()
            last_fetch_time = current_time  # Update the last fetch time
        
        # Update LEDs without delay
        if led_indices:
            if mode == "rainbow":
                update_leds_rainbow()
            else:
                update_leds()
            time.sleep(0.1)
            
def main():
    fetch_img_data_from_firebase()
    while True:
        update_leds_img()
        time.sleep(0.1)
        
    

# Start the program
if __name__ == "__main__":
    main()
    """while True:
        print(adc.read() / 4095)
        time.sleep(1)"""
    
    #fetch_img_data_from_firebase()

