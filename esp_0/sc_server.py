import socket as sc
""" avviare prima questo il server rimane in attesa finché non c'è qualcuno che si connette, poi riceve il messaggio e risponde """
host="" #aperto a tutte le connesione
port=12345
sock = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
sock.bind((host, port))

print(f"Server in ascolto su {host}:{port}...")

sock.listen(1)
conn, addr = sock.accept()
print(f"Connessione accettata da {addr}")
while True:
    data = conn.recv(128)
    if not data:
        break
    print(f"Ricevuto: {data.decode('utf-8')}")
    conn.sendall(b"Ciao dal server!")
conn.close()
sock.close()