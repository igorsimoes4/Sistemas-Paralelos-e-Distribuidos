import socket
import threading

HOST = "0.0.0.0"
PORT = 5000
clientes = []

def cliente_thread(conn, addr):
    print(f"[+] Cliente conectado: {addr}")
    clientes.append(conn)

    try:
        while True:
            msg = conn.recv(1024)

            if not msg:
                break

            print(f"{addr}: {msg.decode()}")

            for cliente in clientes:
                if cliente != conn:
                    cliente.send(msg)

    except:
        pass

    finally:
        clientes.remove(conn)
        conn.close()
        print(f"[-] Cliente saiu: {addr}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Servidor rodando em {HOST}:{PORT}")

while True:
    conn, addr = server.accept()

    thread = threading.Thread(
        target=cliente_thread,
        args=(conn, addr)
    )

    thread.start()