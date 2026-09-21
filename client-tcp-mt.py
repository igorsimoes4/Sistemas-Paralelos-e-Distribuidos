import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

def receber():
    while True:
        try:
            msg = cliente.recv(1024).decode()
            if not msg:
                break
            print(f"\nMensagem: {msg}")
        except:
            break

threading.Thread(target=receber, daemon=True).start()

while True:
    msg = input("Você: ")

    if msg.lower() == "sair":
        break

    cliente.send(msg.encode())

cliente.close()