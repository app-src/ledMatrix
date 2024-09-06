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


# set pixel data to 0 if total rgb luminance is too bright 
def convertWhiteToBlack(data, threshold):
    for index, pixel in enumerate(data):
        if mean(pixel) > threshold:
            data[index] = (0,0,0)

#convert data to 2d array
def return2dArray(data, rowSize=ORIGWIDTH):

    data2d = []
    for n in range(0, (len(data)), rowSize):
        data2d.append(list(data[n: n+rowSize]))
    return data2d
    # print("Height??: " ,len(data2d))
    # print("Width??: ", len(data2d[0]))

def return1dArray(data2d):
    data1d = []
    for row in data2d:
        data1d.extend(row)
    return data1d

def reverseEveryOtherRow(data2d):
    for i in range(1, len(data2d), 2):
        #reverse the array
        data2d[i]=data2d[i][::-1]
 
 
def writeToJson(data1d, filename: str):
    with open(filename, 'w') as outfile:
        json.dump(data1d, outfile)
        print("JSON file created")
    
# print(data2d)

# sends continious stream to simulate upwards scroll on the led matrix of the entire picture    
def simulate_scroll(data2d, SKIPINTERVAL=SKIPINTERVAL, UPDATEDELAY=UPDATEDELAY):
    for n in range(len(data2d)-SKIPINTERVAL):
        print("sneding")
        screenInstance = []
        for row in data2d[n:n+SKIPINTERVAL]:
            for rgb in row:
                screenInstance.append(rgb)
        print(screenInstance, end='\n\n')
        # temp = Image.new('RGB', (ORIGWIDTH, SKIPINTERVAL))
        # temp.putdata(screenInstance)
        # temp.save(f'cropped{n}.jpg')
        print("\n\n\n\n")
        requests.put(url="https://allprojects68-default-rtdb.asia-southeast1.firebasedatabase.app/vaiLED/img.json", json= screenInstance)
        time.sleep(UPDATEDELAY)
        
        


#dump data into a json

import requests
import time

def send_data_in_chunks(data, esp32_ip, chunk_size=1000):
    data = str(data)
    url = f"http://{esp32_ip}"
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    
    for i, chunk in enumerate(chunks, 1):
        headers = {
            'Content-Type': 'text/plain',
            'Chunk-Number': str(i)
        }
        try:
            response = requests.post(url, data=chunk, headers=headers)
            print(f"Chunk {i}/{len(chunks)} sent. Response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending chunk {i}: {str(e)}")
        time.sleep(0.1)  # Small delay between chunks


        
data2d = return2dArray(data)
reverseEveryOtherRow(data2d)
send_data_in_chunks(return1dArray("hi large data here "), esp32_ip)