import socket
import threading

HOST = "0.0.0.0"
PORT = 5000
clientes = []
lock = threading.Lock()

def enviar_para_todos(msg):
    with lock:
        for cliente in clientes[:]:
            try:
                cliente.send(msg.encode())
            except:
                clientes.remove(cliente)

def cliente_thread(conn, addr):
    print(f"[+] Cliente conectado: {addr}")
    with lock: 
        clientes.append(conn)

    try:
        while True:
            msg = conn.recv(1024)

            if not msg:
                break

            print(f"{addr}: {msg.decode()}")
            with lock:
                for cliente in clientes[:]:
                    if cliente != conn:
                        try:
                            cliente.send(msg)
                        except:
                            cliente.remove(cliente)

    except Exception as e:
        print(f"[!] Erro com {addr}: {e}")

    finally:
        with lock:
            if conn in clientes:
                clientes.remove(conn)
    
        conn.close()
        print(f"[-] Cliente saiu: {addr}")

def servidor_chat():
    while True:
        msg = input("Voce: ")
        if msg.lower() == "/sair":
            break
        enviar_para_todos(msg)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print(f"Servidor rodando em {HOST}:{PORT}")

thread_server = threading.Thread(
    target=servidor_chat,
    daemon=True
)

thread_server.start()

while True:
    conn, addr = server.accept()

    thread = threading.Thread(
        target=cliente_thread,
        args=(conn, addr),
        daemon=True
    )

    thread.start()