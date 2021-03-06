# Reads data from Arduino and saves to file
import serial
import pyrebase
import math

config = {
  "apiKey": "AIzaSyDrr76124iABn9Ukw0NgmXFfdnnW_92thg",
  "authDomain": "threedscanner.firebaseapp.com",
  "databaseURL": "https://threedscanner.firebaseio.com",
  "storageBucket": "threedscanner.appspot.com",
}
firebase = pyrebase.initialize_app(config)

db = firebase.database()

ser = serial.Serial("COM3", 9600)
data = []


flag = True
while (flag):
    distance = ser.readline().decode().strip('\r\n')

    if ("End" in distance):
        flag = False

    data.append(distance.split(','))
data.pop(0)
data = data[:-1]

print("Finished")
ser.close()

r = 13

coordinates = []

for i in range (0,len(data)):
    distance = int(data[i][0])
    baseAngle = int(data[i][1])
    sideAngle = int(data[i][2])

    if (r-distance > 0 and distance < r):
        point = []
        #X
        point.append(int((r-distance)*math.cos(sideAngle)*math.cos(270-baseAngle)*1000))
        #Y
        point.append(int((r-distance)*math.sin(sideAngle)*1000))
        #Z
        point.append(int((r-distance)*math.cos(sideAngle)*math.sin(270-baseAngle)*1000))

       coordinates.append(point)


db.child('objects').set(coordinates)
