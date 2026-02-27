from picamera2 import Picamera2
import cv2
import numpy as np
import serial
import time

# ==============================
# SERIAL SETUP
# ==============================

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Attendi reset Arduino

print("Connessione ad Arduino stabilita")

# ==============================
# CAMERA SETUP
# ==============================

picam2 = Picamera2()
picam2.configure(
    picam2.create_preview_configuration(
        main={"format": "RGB888", "size": (320, 240)}
    )
)
picam2.start()

last_direction = None

# ==============================
# MAIN LOOP
# ==============================

while True:
    frame = picam2.capture_array()
    frame = cv2.flip(frame, -1)

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    _, bw = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

    h, w = bw.shape
    roi_y = int(h * 0.7)
    roi = bw[roi_y:h, :]

    ys, xs = np.where(roi == 255)

    if len(xs) > 50:

        cx = int(xs.mean())
        center = w // 2
        tol = w * 0.1

        if cx < center - tol:
            direction = "SINISTRA"
        elif cx > center + tol:
            direction = "DESTRA"
        else:
            direction = "CENTRO"

        if direction != last_direction:
            print("Invio:", direction)
            ser.write((direction + "\n").encode())
            last_direction = direction

        cv2.circle(frame, (cx, roi_y + 5), 5, (0, 0, 255), -1)

    else:
        # Se non vede la linea ? stop
        if last_direction != "STOP":
            print("Invio: STOP")
            ser.write(("STOP\n").encode())
            last_direction = "STOP"

    cv2.line(frame, (0, roi_y), (w, roi_y), (255, 255, 0), 1)
    cv2.line(frame, (w // 2, 0), (w // 2, h), (0, 255, 0), 1)

    cv2.imshow("Line Tracker", frame)
    cv2.imshow("ROI", roi)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# ==============================
# CLEAN EXIT
# ==============================

ser.close()
cv2.destroyAllWindows()
