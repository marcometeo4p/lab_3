import socket as sk
import struct
import soundcard as sc

default_mic = sc.default_microphone()
print(f"Microfono selezionato: {default_mic}\n")

# Acquisizione di 1 secondo di audio (48000 frame a 48kHz)
samplerate = 10000
numframes = 40000
print("Registrazione in corso...")
data = default_mic.record(samplerate=samplerate, numframes=numframes)
print("Array acquisito:")
print(data)
print(f"\nL'array dei dati registrati è lungo {len(data)}\n")

#==========================
host="localhost"
port=12345
sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
sock.connect((host, port))
print(f"Connessione al server stabilita. con {host}:{port}")
#dice che invia solo bytes
#che, merda
data_bytes = data.tobytes()

# 2. Prepariamo la dimensione dei dati da inviare (in modo che il server sappia quanti byte leggere)
data_size = len(data_bytes)
sock.sendall(struct.pack("!I", data_size))
# 3. Inviamo i byte reali dell'array
sock.sendall(data_bytes)
print(
      f"Array inviato con successo! ({data_size} byte, {len(data)} elementi, {len(data_bytes)} byte totali, {len(data_bytes)/4} float32"
      " elementi)"
)
sock.close()