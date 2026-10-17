import socket as sc
import struct
import numpy as np

""" avviare prima questo il server rimane in attesa finché non c'è qualcuno che si connette, poi riceve il messaggio e risponde """

host="" #aperto a tutte le connesione
port=12345
sock = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
sock.bind((host, port))

print(f"Server in ascolto su {host}:{port}...")

sock.listen(1)
conn, addr = sock.accept()
print(f"Connessione accettata da {addr}")

# 1. Riceviamo prima la dimensione dei dati (4 byte per un intero 'I')
raw_size = conn.recv(4)
data_size = struct.unpack("!I", raw_size)[0]
print(f"Dimensione attesa dei dati: {data_size} byte")

# 2. Ora riceviamo i dati reali
dati=[]
bytes_ricevuti=0
while len(dati) < data_size:
    chunk = conn.recv(min(4096, data_size - len(dati)))  # Riceviamo in blocchi di massimo 4096 byte
    if not chunk:
        break
    dati.append(chunk)
    bytes_ricevuti += len(chunk) #per tenere traccia di quanti byte sono stati ricevuti
#dati = conn.recv(data_size)
conn.close()
sock.close()
print(f"Dati ricevuti: {bytes_ricevuti} byte")

# ora abbiamo un'array di pezzi, i chunk, che dobbiamo unire in un unico array di byte
dati_completi = b''.join(dati)

#procediamo a convertire i byte in float32
dati_array = np.frombuffer(dati_completi, dtype=np.float32)

# Lo rimodelliamo nella forma originale (40000 righe, 2 canali)
# Usare -1 dice a NumPy di calcolare automaticamente la prima dimensione
dati_array = dati_array.reshape(-1, 2)

print("Array ricostruito:", dati_array)
print(f"\nL'array dei dati ricevuto è lungo {len(dati_array)}\n")