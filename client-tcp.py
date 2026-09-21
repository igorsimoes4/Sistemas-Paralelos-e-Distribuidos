import socket

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Conectado ao servidor!")

while True:
    mensagem = input("Cliente: ")

    client.send(mensagem.encode())

    if mensagem.lower() == "sair":
        break

    resposta = client.recv(1024).decode()
    print(f"Servidor: {resposta}")

client.close()