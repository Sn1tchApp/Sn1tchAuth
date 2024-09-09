import paho.mqtt.client as mqtt
import time

# Configurações do MQTT
MQTT_HOST = '172.16.4.62'
MQTT_PORT = 1883
MQTT_TOPIC = 'security'
MQTT_USER = 'sn1tchapp'
MQTT_PASSWORD = 'sn1tchapp'
LOG_FILE = '/home/ec2-user/interoperabilidade2/security.log'

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def send_to_mqtt(log_line):
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_start()
    client.publish(MQTT_TOPIC, log_line)
    client.loop_stop()
    client.disconnect()

def monitor_log_file():
    with open(LOG_FILE, 'r') as log_file:
        log_file.seek(0, 2)  # Move to the end of the file
        while True:
            line = log_file.readline()
            if line:
                send_to_mqtt(line.strip())
            time.sleep(1)

if __name__ == '__main__':
    monitor_log_file()
