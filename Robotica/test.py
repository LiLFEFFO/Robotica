import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # tempo per il reset dell'Arduino

while True:
    cmd = input("Comando da inviare: ")
    ser.write((cmd + "\n").encode())
    print("Inviato:", cmd)
