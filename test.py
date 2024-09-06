import requests
import json

def send_data(data, esp32_ip):
    url = f"http://{esp32_ip}"
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error sending data:", e)

if __name__ == "__main__":
    # Replace with your ESP32's IP address
    esp32_ip = "172.5.0.106"
    
    # Example data to send
    data_to_send = [
        [177, 3, 2],
        [183, 1, 0],
        [192, 0, 0],
        [197, 0, 0],
        [194, 0, 0],
        [188, 0, 0],
        [181, 2, 0],
        [178, 2, 2],
        [177, 0, 9],
        [182, 0, 15],
        [184, 0, 14],
        [179, 0, 4],
        [186, 4, 3],
        [187, 2, 0]
    ]
    
    send_data(data_to_send, esp32_ip)