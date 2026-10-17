import socket as sk
import struct
import soundcard as sc

#==========ACQUISIZIONE================
default_mic = sc.default_microphone()
print(f"Microfono selezionato: {default_mic}\n")

# Acquisizione di 1 secondo di audio (48000 frame a 48kHz)
samplerate = 48000
numframes = 48000*5
print("Registrazione in corso...")
data = default_mic.record(samplerate=samplerate, numframes=numframes)
print("Array acquisito:")
print(data)
print(f"\nL'array dei dati registrati è lungo {len(data)}\n")

#==========TRASMISSIONE================
host="localhost"
port=12345
sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
sock.connect((host, port))
print(f"Connessione al server stabilita. con {host}:{port}")
#dice che invia solo bytes
data_bytes = data.tobytes()

# 2. Prepariamo la dimensione dei dati da inviare (in modo che il server sappia quanti byte leggere)
# protocollo 1) --------------dimensione attesa------------
data_size = len(data_bytes)

print("costruiamo header contenente: frequenza, numero di frame e dimensione attesa dei dati")
header = struct.pack("!III", samplerate, numframes, data_size)
sock.sendall(header)
# protocollo 2) --------------invio dati reali------------
sock.sendall(data_bytes)
print(
      f"Array inviato con successo! ({data_size} byte, {len(data)} elementi, {len(data_bytes)} byte totali, {len(data_bytes)/4} float32"
      " elementi)"
)

#protocollo 3) --------------ricezione conferma------------
response = sock.recv(1024)
print(f"Risposta dal server: {bytes(response).decode('utf-8')}")
sock.close()