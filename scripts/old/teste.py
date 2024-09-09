import paho.mqtt.client as mqtt
import time

# Configurações do MQTT
MQTT_HOST = '172.16.4.62'
MQTT_PORT = 1883
MQTT_TOPIC = 'security'
MQTT_USER = 'producer'
MQTT_PASSWORD = 'sn1tchapp'

# Cria uma instância do cliente MQTT
client = mqtt.Client()

# Callback de conexão
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected successfully to MQTT Broker at {MQTT_HOST}:{MQTT_PORT}")
    else:
        print(f"Failed to connect, return code {rc}")

# Callback de publicação
def on_publish(client, userdata, mid):
    print(f"Message {mid} published.")

# Configura as credenciais de autenticação
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_publish = on_publish

# Conecta ao broker MQTT
client.connect(MQTT_HOST, MQTT_PORT, 60)

# Inicia o loop do cliente
client.loop_start()

# Enviar mensagens de teste
def send_test_messages():
    messages = [
        "Test message 1",
        "Test message 2",
        "Test message 3",
        "Test message 4",
        "Test message 5"
    ]

    for msg in messages:
        print(f"Sending: {msg}")
        result = client.publish(MQTT_TOPIC, msg, qos=1)
        result.wait_for_publish()  # Espera a confirmação da publicação
        time.sleep(1)  # Pequena pausa entre os envios

if __name__ == '__main__':
    print(f"Starting to send test messages to {MQTT_TOPIC}")
    send_test_messages()
    client.loop_stop()
    client.disconnect()
