
import socket
import threading

HOST = "0.0.0.0"
PORT = 5000
CHAVE = 3

clientes = []
lock = threading.Lock()


def criptografar(msg):
    resultado = ""

    for char in msg:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            resultado += chr((ord(char) - base + CHAVE) % 26 + base)
        else:
            resultado += char

    return resultado.encode("utf-8")


def descriptografar(msg):
    texto = msg.decode("utf-8")
    resultado = ""

    for char in texto:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            resultado += chr((ord(char) - base - CHAVE) % 26 + base)
        else:
            resultado += char

    return resultado


def enviar_para_todos(msg):
    dados = criptografar(msg)

    with lock:
        for cliente in clientes[:]:
            try:
                cliente.sendall(dados + b"\n")
            except:
                clientes.remove(cliente)


def cliente_thread(conn, addr):
    print(f"[+] Cliente conectado: {addr}")

    with lock:
        clientes.append(conn)

    buffer = b""

    try:
        while True:
            dados = conn.recv(1024)

            if not dados:
                break

            buffer += dados

            while b"\n" in buffer:
                msg, buffer = buffer.split(b"\n", 1)

                if not msg:
                    continue

                texto = descriptografar(msg)
                print(f"{addr}: {texto}")

                # Repassa a mensagem criptografada
                enviar_para_todos(texto)

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
        msg = input("Você: ")

        if msg.lower() == "sair":
            break

        enviar_para_todos(msg)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print(f"Servidor rodando em {HOST}:{PORT}")

threading.Thread(
    target=servidor_chat,
    daemon=True
).start()

try:
    while True:
        conn, addr = server.accept()

        threading.Thread(
            target=cliente_thread,
            args=(conn, addr),
            daemon=True
        ).start()

except KeyboardInterrupt:
    print("\nEncerrando servidor...")

finally:
    server.close()