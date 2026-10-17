import socket as sc
import struct
import numpy as np
import soundcard as scd
import matplotlib.pyplot as plt
""" avviare prima questo il server rimane in attesa finché non c'è qualcuno che si connette, poi riceve il messaggio e risponde """

host="" #aperto a tutte le connesione
port=12345
sock = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
sock.bind((host, port))

print(f"Server in ascolto su {host}:{port}...")

sock.listen(1)
conn, addr = sock.accept()
print(f"Connessione accettata da {addr}")

# protocollo 1) --------------ricezione metadati e dimensione------------
# Leggiamo 12 byte per i 3 interi (samplerate, numframes, data_size)
print("Ci prepariamo a ricevere e decodificare l'header contenente: frequenza, numero di frame e dimensione attesa dei dati")
raw_header = conn.recv(12)
samplerate, numframes, data_size = struct.unpack("!III", raw_header)

print(f"Ricevuto - Frequenza: {samplerate}Hz, Frames: {numframes}")
print(f"Dimensione attesa dei dati: {data_size} byte")

# protocollo 2) --------------ricezione dati reali------------
dati = []
bytes_ricevuti = 0

while bytes_ricevuti < data_size:
    # Calcoliamo quanti byte mancano usando bytes_ricevuti, NON len(dati)
    rimanenti = data_size - bytes_ricevuti
    chunk = conn.recv(min(4096, rimanenti))
    
    if not chunk:
        break
        
    dati.append(chunk)
    bytes_ricevuti += len(chunk)  # Aggiorniamo il contatore dei byte reali

# protocollo 3) --------------invio conferma------------
if bytes_ricevuti == data_size:
    conn.sendall(b"OK! Ricevuti tutti i dati correttamente.")
else:
    conn.sendall(b"ERRORE! Non sono stati ricevuti tutti i dati previsti.")

conn.close()
sock.close()
print(f"Dati ricevuti: {bytes_ricevuti} byte")

# ora abbiamo un'array di pezzi, i chunk, che dobbiamo unire in un unico array di byte
dati_completi = b''.join(dati)

#procediamo a convertire i byte in float32
dati_array = np.frombuffer(dati_completi, dtype=np.float32)

# Lo rimodelliamo nella forma originale (240000 righe, 2 canali)
# Usare -1 dice a NumPy di calcolare automaticamente la prima dimensione
dati_array = dati_array.reshape(-1, 2)

print("Array ricostruito:", dati_array)
print(f"\nL'array dei dati ricevuto è lungo {len(dati_array)}\n")

#============GRAFICO================
if dati_array.ndim > 1:
  audio_signal = dati_array[:, 0]
else:
  audio_signal = dati_array

duration = len(audio_signal) / samplerate
time_axis = np.linspace(0, duration, len(audio_signal))

plt.figure(figsize=(10, 4))
plt.plot(time_axis, audio_signal, color='b', alpha=0.6)
plt.title('Segnale Audio nel Dominio del Tempo')
plt.xlabel('Tempo (secondi)')
plt.ylabel('Ampiezza')
plt.grid(True)
# Aggiungi block=False per dire allo script di non fermarsi
plt.show(block=False) 
plt.savefig("audio_plot.png")
# Aggiungi una piccola pausa per dare tempo all'interfaccia grafica di disegnare la finestra
plt.pause(0.5)

#==========RIPRODUZIONE================
default_speaker = scd.default_speaker()
print(f"Speaker selezionato: {default_speaker}\n")

# Riproduzione sicura dei dati
max_val = np.max(np.abs(dati_array))
if max_val > 0:
  normalized_data = dati_array / max_val
  print("Riproduzione in corso...")
  default_speaker.play(samplerate=samplerate, data=normalized_data)
else:
  print(
      "L'audio registrato è completamente silenzioso (nessun picco rilevato)."
  )
plt.show()