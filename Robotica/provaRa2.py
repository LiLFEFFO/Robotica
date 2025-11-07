import cv2
import numpy as np

# Apri la camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Riduci la dimensione per maggiore velocità
    frame = cv2.resize(frame, (320, 240))

    # Converto in grigio
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Applico un filtro gaussiano per ridurre il rumore
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # Threshold per ottenere solo la linea nera
    _, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

    # Prendo solo la parte bassa dell’immagine
    roi = thresh[120:240, :]

    # Trovo i contorni
    contours, _ = cv2.findContours(roi, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Prendo il contorno più grande
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] != 0:
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])

            # Mostra la linea centrale
            cv2.circle(frame, (cx, cy+120), 5, (0,0,255), -1)

            # Logica di direzione
            if cx < 120:
                direction = "SINISTRA"
            elif cx > 200:
                direction = "DESTRA"
            else:
                direction = "DRITTO"
            print("Direzione:", direction)

    cv2.imshow("Frame", frame)
    cv2.imshow("Threshold", thresh)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
