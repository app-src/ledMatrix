import machine, neopixel

n = 210
p = 27

np = neopixel.NeoPixel(machine.Pin(p), n)

# Turn off all LEDs
for i in range(n):
    np[i] = (0, 0, 0)
    
    
O=[]    
O = [34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 35, 69, 104, 70, 105, 139, 174, 140, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209]

#O = [1, 2, 3, 4, 5, 6, 8, 11, 16, 17, 18, 19, 21, 22, 32, 37, 39, 42, 43, 45, 48, 50, 51, 52, 53, 58, 59, 60, 64, 71, 72, 77, 80, 81, 90, 91, 92, 93
#O = [120,12,14,35,17]



for i in range(0,n):
    if i in O:
        np[i] = (255,255,0)

np.write()
