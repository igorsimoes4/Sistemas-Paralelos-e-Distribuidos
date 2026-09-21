
import socket
import threading

HOST = "127.0.0.1"
PORT = 5000
CHAVE = 3

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))


def criptografar(msg):
    resultado = ""

    for char in msg:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            resultado += chr(
                (ord(char) - base + CHAVE) % 26 + base
            )
        else:
            resultado += char

    return resultado.encode("utf-8")


def descriptografar(msg):
    texto = msg.decode("utf-8")
    resultado = ""

    for char in texto:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            resultado += chr(
                (ord(char) - base - CHAVE) % 26 + base
            )
        else:
            resultado += char

    return resultado


def receber():
    buffer = b""

    while True:
        try:
            dados = cliente.recv(1024)

            if not dados:
                break

            buffer += dados

            while b"\n" in buffer:
                msg, buffer = buffer.split(b"\n", 1)

                if msg:
                    print(f"\nMensagem: {descriptografar(msg)}")

        except:
            break


threading.Thread(target=receber, daemon=True).start()

try:
    while True:
        msg = input("Você: ")

        if msg.lower() == "sair":
            break

        cliente.sendall(criptografar(msg) + b"\n")

finally:
    cliente.close()