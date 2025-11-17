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

    # Ruota di 180 gradi
    frame = cv2.rotate(frame, cv2.ROTATE_180)

    # ======== RICONOSCIMENTO LINEA ========
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)

    h, w = thresh.shape
    roi = thresh[int(h * 0.6):h, :]

    contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            cv2.circle(frame, (cx, cy + int(h * 0.6)), 5, (0, 0, 255), -1)
            cv2.drawContours(frame[int(h * 0.6):h, :], [c], -1, (0, 255, 0), 2)

            print("Linea trovata alla X =", cx)
        else:
            print("Linea non trovata")
    else:
        print("Nessun contorno trovato")

    # ======== RICONOSCIMENTO PALLINE VIVO/MORTO ========
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray_for_circles = cv2.medianBlur(gray, 5)

    # Cerca palline (se rotonde)
    circles = cv2.HoughCircles(
        gray_for_circles,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=40,
        param1=80,
        param2=20,
        minRadius=10,
        maxRadius=60
    )

    if circles is not None:
        circles = np.uint16(np.around(circles))

        for (x, y, r) in circles[0, :]:
            # Estrai il colore medio nella pallina
            mask = np.zeros(gray.shape, dtype=np.uint8)
            cv2.circle(mask, (x, y), r, 255, -1)

            mean_val = cv2.mean(gray, mask=mask)[0]

            # Soglie regolabili
            if mean_val > 180:
                stato = "VIVO (pallina argentata)"
                color = (0, 255, 255)  # giallo
            elif mean_val < 60:
                stato = "MORTO (pallina nera)"
                color = (0, 0, 255)  # rosso
            else:
                stato = "Sconosciuto"
                color = (255, 255, 255)

            # Disegna la pallina
            cv2.circle(frame, (x, y), r, color, 2)
            cv2.putText(frame, stato, (x - r, y - r - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            print(f"Pallina trovata: {stato}, luminosità={mean_val:.1f}")

    # ======== MOSTRA FINESTRE ========
    cv2.imshow("Frame", frame)
    cv2.imshow("Threshold", roi)

    # ESC per uscire
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
