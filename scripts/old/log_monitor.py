import pika
import paho.mqtt.publish as publish
import time

# Configurações do RabbitMQ
RABBITMQ_HOST = '172.16.4.62:5672'
RABBITMQ_QUEUE = 'security'
LOG_FILE = '/home/ec2-user/interoperabilidade2/security.log'

def send_to_rabbitmq(log_line):
    publish.single(RABBITMQ_QUEUE, log_line, hostname=RABBITMQ_HOST)

def monitor_log_file():
    with open(LOG_FILE, 'r') as log_file:
        log_file.seek(0, 2)  # Move to the end of the file
        while True:
            line = log_file.readline()
            if line:
                send_to_rabbitmq(line.strip())
            time.sleep(1)

if __name__ == '__main__':
    monitor_log_file()
