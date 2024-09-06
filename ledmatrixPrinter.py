#load image file from directory

from PIL import Image
from statistics import mean
import time
import requests
import json

ORIGWIDTH = 35
ORIGHEIGHT = 30
SKIPINTERVAL = 6
UPDATEDELAY = 2 #delay between updates sent to firebase


# Replace with your ESP32's IP address
esp32_ip = "172.5.0.106"
    


img = Image.open('star.jpg') #use any jpg that is of 35 x 30 pixels (width x height)
data= list(img.getdata())

data2d = []

# set pixel data to 0 if total rgb luminance is too bright 
for index, pixel in enumerate(data):
    print(pixel)
    if mean(pixel) > 250:
        data[index] = (0,0,0)

#convert data to 2d array
for n in range(0, (len(data)), ORIGWIDTH):
    data2d.append(list(data[n: n+ORIGWIDTH]))
# print("Height??: " ,len(data2d))
# print("Width??: ", len(data2d[0]))

for i in range(1, len(data2d), 2):
    #reverse the array
    data2d[i]=data2d[i][::-1]
 
print(data2d)

#sends continious stream to simulate upwards scroll on the led matrix of the entire picture    
# for n in range(len(data2d)-SKIPINTERVAL):
#     print("sneding")
#     screenInstance = []
#     for row in data2d[n:n+SKIPINTERVAL]:
#         for rgb in row:
#             screenInstance.append(rgb)
#     print(screenInstance, end='\n\n')
#     # temp = Image.new('RGB', (ORIGWIDTH, SKIPINTERVAL))
#     # temp.putdata(screenInstance)
#     # temp.save(f'cropped{n}.jpg')
#     print("\n\n\n\n")
#     requests.put(url="https://allprojects68-default-rtdb.asia-southeast1.firebasedatabase.app/vaiLED/img.json", json= screenInstance)
#     time.sleep(UPDATEDELAY)
    
print(len(data))
#dump data into a json

def send_data(data, esp32_ip):
    url = f"http://{esp32_ip}"
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error sending data:", e)


with open('output2.json', 'w') as outfile:
    json.dump(data2d, outfile)
    print("JSON file created")


send_data(data_to_send, esp32_ip)    