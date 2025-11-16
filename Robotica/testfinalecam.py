from picamera2 import Picamera2
import cv2
import numpy as np

# --- Inizializzazione camera ---
picam2 = Picamera2()

config = picam2.create_preview_configuration(
    main={"format": "RGB888", "size": (640, 480)},
)
picam2.configure(config)
picam2.start()

print("Camera avviata. Premi ESC per uscire.")

while True:
    # Acquisisci frame dalla camera
    frame = picam2.capture_array()
    
    #Ruota di 180 gradi per vedere giusto
    frame = cv2.rotate(frame, cv2.ROTATE_180)

    # Converti in scala di grigi
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # Blur per ridurre rumore
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold per linea scura (invertita)
    _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)

    h, w = thresh.shape

    # Considera solo parte bassa (roi)
    roi = thresh[int(h * 0.6):h, :]

    # Cerca contorni
    contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Contorno più grande = linea principale
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Disegna il centroide
            cv2.circle(frame, (cx, cy + int(h * 0.6)), 5, (0, 0, 255), -1)
            cv2.drawContours(frame[int(h * 0.6):h, :], [c], -1, (0, 255, 0), 2)

            print("Linea trovata alla X =", cx)
        else:
            print("Linea non trovata")
    else:
        print("Nessun contorno trovato")

    # Mostra finestre debug
    cv2.imshow("Frame", frame)
    cv2.imshow("Threshold", roi)

    # ESC per uscire
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
