import paho.mqtt.client as mqtt
import time

# Configurações do MQTT
MQTT_HOST = 'localhost'
#MQTT_HOST = '18.231.148.22'
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

# Callback para tratar desconexões
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"Unexpected disconnection. Code: {rc}")
    else:
        print("Disconnected successfully.")

# Callback para log de erros
def on_log(client, userdata, level, buf):
    print(f"Log: {buf}")

# Configura as credenciais de autenticação
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect
client.on_log = on_log

# Conecta ao broker MQTT
client.connect(MQTT_HOST, MQTT_PORT, 60)

# Inicia o loop do cliente
client.loop_start()

# Enviar mensagens de teste
def send_test_messages():
    messages = [
        "LNXEXEC-02 sshd[23150]: Failed password for julio from 172.24.0.69 port 47370 ssh2",
        "LNXEXEC-01 sshd[1761]: Failed password for julia from 172.24.0.69 port 47640 ssh2",
        "LNXEXEC-01 sshd[1761]: Failed password for fernando from 172.24.0.69 port 47640 ssh2",
        "LNXEXEC-02 sshd[9525]: Failed password for francisco from 172.24.0.69 port 46684 ssh2",
        "LNXEXEC-01 sshd[7741]: Failed password for marcos from 172.24.0.69 port 36296 ssh2",
        "LNXEXEC-01 sshd[7741]: Failed password for michele from 172.24.0.69 port 36296 ssh2",
        "LNXEXEC-01 sshd[32279]: Failed password for ferdando_bezerra from 172.24.0.69 port 44606 ssh2",
        "LNXEXEC-01 sshd[31418]: Failed password for paulo from 172.24.0.69 port 37244 ssh2",
        "LNXEXEC-01 sshd[31418]: Failed password for pedro_eugenio from 172.24.0.69 port 37244 ssh2",
        "LNXEXEC-01 sshd[31418]: Failed password for emanuel from 172.24.0.69 port 37244 ssh2",
        "LNXEXEC-01 sshd[31418]: Failed password for pedro_trajano from 172.24.0.69 port 37244 ssh2",
        "LNXEXEC-01 sshd[31418]: Failed password for henrique from 172.24.0.69 port 37244 ssh2",
        "LNXEXEC-01 sshd[31418]: Failed password for fernando_coelho from 172.24.0.69 port 37244 ssh2",
        "srv01 sshd[8830]: Failed password for invalid marcos kkls from 172.24.30.40 port 50734 ssh2",
        "srv01 sshd[8830]: Failed password for invalid michele jkpl from 172.24.30.40 port 50734 ssh2"
    ]

    for msg in messages:
        print(f"Sending: {msg}")
        result = client.publish(MQTT_TOPIC, msg, qos=1)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            print(f"Failed to send message. Result code: {result.rc}")
        result.wait_for_publish()  # Espera a confirmação da publicação
        time.sleep(1)  # Pequena pausa entre os envios

if __name__ == '__main__':
    print(f"Starting to send test messages to {MQTT_TOPIC}")
    send_test_messages()
    client.loop_stop()
    client.disconnect()
