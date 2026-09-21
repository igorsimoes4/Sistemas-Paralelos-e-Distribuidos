"""
Consumer (Subscriber) MQTT
Conecta ao broker público broker.emqx.io e fica escutando
mensagens de um tópico.

Instalação necessária:
    pip install paho-mqtt
"""

import random
from paho.mqtt import client as mqtt_client

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "python/mqtt/test"
CLIENT_ID = f"python-mqtt-subscriber-{random.randint(0, 100000)}"


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected successfully to MQTT Broker!")
        result = client.subscribe(TOPIC, qos=1)
        print(f"Inscrito no tópico: {TOPIC} (resultado: {result})")
    else:
        print(f"Failed to connect, return code {rc}")


def on_subscribe(client, userdata, mid, reason_codes, properties=None):
    print(f"Confirmação de subscribe recebida (mid={mid}, codes={reason_codes})")


def on_message(client, userdata, msg):
    print(f"Received: '{msg.payload.decode()}' from topic: '{msg.topic}'")


def on_log(client, userdata, level, buf):
    print(f"[LOG] {buf}")


def run():
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, CLIENT_ID)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message

    print(f"Conectando em {BROKER}:{PORT} ...")
    client.connect(BROKER, PORT)

    print("Aguardando mensagens... (Ctrl+C para sair)")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nEncerrando consumer...")
        client.disconnect()


if __name__ == "__main__":
    run()