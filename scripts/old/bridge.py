import paho.mqtt.client as mqtt
from confluent_kafka import Producer

# Configurações MQTT
MQTT_BROKER = 'localhost'
MQTT_PORT = 5672
MQTT_TOPIC = 'security'

# Configurações Kafka
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'security'

# Inicializa o produtor Kafka
producer = Producer({'bootstrap.servers': KAFKA_BROKER})

# Função callback quando uma mensagem MQTT é recebida
def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    print(f"Recebido MQTT: {payload}")
    producer.produce(KAFKA_TOPIC, payload)
    producer.flush()

# Configura o cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.subscribe(MQTT_TOPIC)

# Inicia o loop de processamento de mensagens MQTT
mqtt_client.loop_forever()
