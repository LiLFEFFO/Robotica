import cv2
import serial
import time

# Apri seriale verso Arduino
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Attendi che l'Arduino si resetti

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # --- Elaborazione per seguire la linea ---
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
    M = cv2.moments(thresh)

    if M["m00"] > 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        
        error = cx - frame.shape[1] // 2

        # Controllo proporzionale semplice
        Kp = 0.1
        correction = int(Kp * error)

        left_speed = 100 - correction
        right_speed = 100 + correction

        # Limiti
        left_speed = max(min(left_speed, 255), 0)
        right_speed = max(min(right_speed, 255), 0)

        cmd = f"{left_speed},{right_speed}\n"
        ser.write(cmd.encode())
    else:
        # Nessuna linea trovata → stop
        ser.write(b"0,0\n")

cap.release()
