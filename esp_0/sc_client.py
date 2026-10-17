import socket as stocazzo
host="localhost"
port=12345
sock = stocazzo.socket(stocazzo.AF_INET, stocazzo.SOCK_STREAM)
sock.connect((host, port))

sock.sendall(b"saluta salame!!")

dito=sock.recv(1024)
print(f"Ricevuto: {dito.decode('utf-8')}")

sock.close()