"""
Publisher MQTT (interativo)
Conecta ao broker público broker.emqx.io e publica mensagens
digitadas pelo usuário no terminal.

Instalação necessária:
    pip install paho-mqtt
"""

import random
from paho.mqtt import client as mqtt_client

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "python/mqtt/test"
CLIENT_ID = f"python-mqtt-publisher-{random.randint(0, 100000)}"


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected successfully to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")


def on_publish(client, userdata, mid, reason_code=None, properties=None):
    print(f"Confirmação de publish recebida (mid={mid})")


def run():
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, CLIENT_ID)
    client.on_connect = on_connect
    client.on_publish = on_publish

    print(f"Conectando em {BROKER}:{PORT} ...")
    client.connect(BROKER, PORT)
    client.loop_start()

    print("Digite a mensagem e pressione Enter para publicar.")
    print("Digite 'sair' para encerrar.\n")

    try:
        while True:
            mensagem = input("Mensagem: ")
            if mensagem.lower() == "sair":
                break
            result = client.publish(TOPIC, mensagem, qos=1)
            result.wait_for_publish()
            print(f"Publicado: {mensagem} (mid={result.mid})")
    except KeyboardInterrupt:
        pass
    finally:
        print("\nEncerrando publisher...")
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    run()