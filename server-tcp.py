import socket

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"Servidor aguardando conexão na porta {PORT}...")
conn, addr = server.accept()
print(f"Cliente conectado: {addr}")

while True:
    mensagem = conn.recv(1024).decode()

    if not mensagem or mensagem.lower() == "sair":
        break

    print(f"Cliente: {mensagem}")

    resposta = input("Servidor: ")
    conn.send(resposta.encode())

conn.close()
server.close()