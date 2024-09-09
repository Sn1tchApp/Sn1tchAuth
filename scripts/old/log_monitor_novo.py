import paho.mqtt.client as mqtt
import time

# Configurações do MQTT
MQTT_HOST = '172.16.4.62'
MQTT_PORT = 1883
MQTT_TOPIC = 'security'
MQTT_USER = 'producer'
MQTT_PASSWORD = 'sn1tchapp'
LOG_FILE = '/home/ec2-user/interoperabilidade2/security.log'

# Cria uma instância do cliente MQTT
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

# Configura as credenciais de autenticação
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_connect = on_connect

# Conecta ao broker MQTT
client.connect(MQTT_HOST, MQTT_PORT, 60)

def send_to_mqtt(log_line):
    # Publica a mensagem no tópico
    client.publish(MQTT_TOPIC, log_line)

def monitor_log_file():
    client.loop_start()  # Inicia o loop do cliente em uma thread separada
    with open(LOG_FILE, 'r') as log_file:
        log_file.seek(0, 2)  # Move para o final do arquivo
        while True:
            line = log_file.readline()
            if line:
                send_to_mqtt(line.strip())
            time.sleep(1)
    client.loop_stop()  # Para o loop do cliente

if __name__ == '__main__':
    monitor_log_file()
