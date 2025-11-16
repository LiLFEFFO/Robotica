# Robotica

testfinalecam.py è lo script principale iniziale e una volta eseguito:
-Acquisisce continuamente i frame dalla Picamera2.
-Li ruota e converte in scala di grigi.
-Applica un blur per ridurre il rumore.
-Applica un threshold invertito per isolare la linea scura come oggetto bianco.
-Estrae solo la parte bassa dell’immagine.
-Trova i contorni → prende quello più grande (la linea).
-Calcola il centroide della linea.
-Lo disegna sul frame e stampa la posizione X della linea.
-Mostra finestre di debug.
