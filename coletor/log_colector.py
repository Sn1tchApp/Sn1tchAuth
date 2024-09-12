import paho.mqtt.client as mqtt
import time

# Configurações do MQTT
MQTT_HOST = '172.16.4.62'
#MQTT_HOST = '18.231.148.22'
MQTT_PORT = 1883
MQTT_TOPIC = 'security'
MQTT_USER = 'producer'
MQTT_PASSWORD = 'sn1tchapp'
LOG_FILE = '/home/ec2-user/interoperabilidade2/security.log'

# Cria uma instância do cliente MQTT
client = mqtt.Client()

# Callback de conexão
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected successfully to MQTT Broker at {MQTT_HOST}:{MQTT_PORT}")
    else:
        print(f"Failed to connect, return code {rc}")

# Callback de desconexão
def on_disconnect(client, userdata, rc):
    print(f"Disconnected from MQTT Broker with result code {rc}")

# Callback de publicação
def on_publish(client, userdata, mid):
    print(f"Message {mid} published.")

# Configura as credenciais de autenticação
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

# Conecta ao broker MQTT
client.connect(MQTT_HOST, MQTT_PORT, 60)

def send_to_mqtt(log_line):
    print(f"Sending line: {log_line}")
    result = client.publish(MQTT_TOPIC, log_line, qos=1)
    if result.rc != mqtt.MQTT_ERR_SUCCESS:
        print(f"Failed to send message. Result code: {result.rc}")
    else:
        print(f"Message sent to {MQTT_TOPIC}")

def monitor_log_file():
    print(f"Monitoring log file: {LOG_FILE}")
    client.loop_start()  # Inicia o loop do cliente em uma thread separada
    with open(LOG_FILE, 'r') as log_file:
        log_file.seek(0, 2)  # Move para o final do arquivo
        while True:
            line = log_file.readline()
            if line:
                send_to_mqtt(line.strip())
            else:
                print("No new line in log file, sleeping for 1 second...")
            time.sleep(1)  # Pequena pausa para evitar alta carga no sistema
    client.loop_stop()  # Para o loop do cliente

if __name__ == '__main__':
    print(f"Starting log monitor with settings:")
    print(f"MQTT Broker: {MQTT_HOST}:{MQTT_PORT}")
    print(f"MQTT User: {MQTT_USER}")
    print(f"MQTT Topic: amq.topic")
    print(f"MQTT Topic Routing key: {MQTT_TOPIC}")
    print(f"Log File: {LOG_FILE}")
    monitor_log_file()
