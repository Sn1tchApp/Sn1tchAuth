from confluent_kafka import Consumer, KafkaException, Producer
import requests
import re
from datetime import datetime, timedelta
import time
import json

# Configurações do Kafka (Consumer e Producer)
conf_consumer = {
    'bootstrap.servers': '172.16.4.62:9092',
    'group.id': 'brute-force-detector',
    'auto.offset.reset': 'earliest'
}

conf_producer = {
    'bootstrap.servers': '172.16.4.62:9092'
}

consumer = Consumer(conf_consumer)
producer = Producer(conf_producer)
consumer.subscribe(['security'])

# Configurações do Telegram
TELEGRAM_API_URL = 'https://api.telegram.org/bot6838291448:AAFWetNkMRtqFk9q1y-YyqGzZWUU7n7Qzm8/sendMessage'
CHAT_ID = '-1002479259032'

# Padrão regex para detectar brute force em logs SSH
brute_force_pattern = re.compile(
    r'(?P<server>\S+) sshd\[\d+\]: Failed password for (invalid user )?(?P<user>[\w_-]+) from (?P<ip>[\d.]+) port \d+ ssh2'
)

# Contadores de eventos e usuários
event_count_by_server = {}
global_attempts = {}
attempts_by_ip = {}

# Limite de tempo para verificar brute force (últimos 1 minuto)
TIME_LIMIT = timedelta(minutes=1)
INTERVAL = timedelta(minutes=1)

def send_telegram_message(message):
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(TELEGRAM_API_URL, json=payload)
    if response.status_code != 200:
        print(f'Error sending message: {response.text}')
    else:
        print("Mensagem enviada com sucesso ao Telegram.")

def send_kafka_alert(alert_data):
    try:
        producer.produce('alerts', json.dumps(alert_data).encode('utf-8'), key='attemps')
        producer.flush()
        print(f'Alerta enviado ao tópico Kafka: {alert_data}')
    except Exception as e:
        print(f'Erro ao enviar alerta ao Kafka: {e}')

def parse_log(log):
    match = brute_force_pattern.match(log)
    if match:
        server = match.group('server')
        user = match.group('user')
        ip = match.group('ip')
        return {
            'timestamp': datetime.now(),
            'server': server,
            'user': user,
            'ip': ip
        }
    return None

def detect_brute_force(parsed_log):
    server = parsed_log['server']
    user = parsed_log['user']
    ip = parsed_log['ip']
    timestamp = parsed_log['timestamp']

    # Atualizar tentativas por servidor
    if server not in event_count_by_server:
        event_count_by_server[server] = {}

    if user not in event_count_by_server[server]:
        event_count_by_server[server][user] = {'count': 0, 'ips': set(), 'timestamp': timestamp}
    
    event_count_by_server[server][user]['count'] += 1
    event_count_by_server[server][user]['ips'].add(ip)

    # Atualizar tentativas globais (por usuário independentemente do servidor)
    if user not in global_attempts:
        global_attempts[user] = {'count': 0, 'ips': set(), 'servers': set(), 'timestamp': timestamp}
    
    global_attempts[user]['count'] += 1
    global_attempts[user]['ips'].add(ip)
    global_attempts[user]['servers'].add(server)

    # Atualizar tentativas por IP (para detecção de password spray)
    if ip not in attempts_by_ip:
        attempts_by_ip[ip] = {'users': {}, 'timestamp': timestamp}
    
    if user not in attempts_by_ip[ip]['users']:
        attempts_by_ip[ip]['users'][user] = 0
    
    attempts_by_ip[ip]['users'][user] += 1

def process_alerts():
    now = datetime.now()

    # Verificar brute force por servidor
    for server, users in list(event_count_by_server.items()):
        for user, data in list(users.items()):
            if now - data['timestamp'] >= TIME_LIMIT:
                if data['count'] >= 3:
                    message = (
                        f"🚨 Brute Force Detectado no servidor {server}!\n"
                        f"Usuário: {user}\n"
                        f"IP de Origem: {', '.join(data['ips'])}\n"
                        f"Tentativas: {data['count']}\n"
                    )
                    send_telegram_message(message)
                    
                    # Enviar alerta para o tópico Kafka
                    alert_data = {
                        'type': 'brute_force',
                        'server': server,
                        'user': user,
                        'ip': list(data['ips']),
                        'count': data['count'],
                        'timestamp': str(datetime.now())
                    }
                    send_kafka_alert(alert_data)
                    
                # Resetar contagem
                event_count_by_server[server][user]['count'] = 0

    # Verificar brute force global
    for user, data in list(global_attempts.items()):
        if now - data['timestamp'] >= TIME_LIMIT:
            if data['count'] >= 5 and len(data['servers']) > 1:
                message = (
                    f"🚨 Brute Force Global Detectado!\n"
                    f"Usuário: {user}\n"
                    f"IPs de Origem: {', '.join(data['ips'])}\n"
                    f"Servidores Alvo: {', '.join(data['servers'])}\n"
                    f"Tentativas: {data['count']}\n"
                )
                send_telegram_message(message)

                # Enviar alerta para o tópico Kafka
                alert_data = {
                    'type': 'global_brute_force',
                    'user': user,
                    'ips': list(data['ips']),
                    'servers': list(data['servers']),
                    'count': data['count'],
                    'timestamp': str(datetime.now())
                }
                send_kafka_alert(alert_data)
                
            # Resetar contagem
            global_attempts[user]['count'] = 0
            global_attempts[user]['servers'].clear()

    # Verificar password spray
    ip_keys_to_remove = []
    for ip, data in attempts_by_ip.items():
        if now - data['timestamp'] >= TIME_LIMIT:
            if len(data['users']) > 5 and any(count > 2 for count in data['users'].values()):
                message = (
                    f"🚨 Password Spray Detectado!\n"
                    f"IP de Origem: {ip}\n"
                    f"Usuários Tentados: {', '.join(data['users'].keys())}\n"
                    f"Tentativas por Usuário: {', '.join([f'{user}: {count}' for user, count in data['users'].items()])}\n"
                )
                send_telegram_message(message)

                # Enviar alerta para o tópico Kafka
                alert_data = {
                    'type': 'password_spray',
                    'ip': ip,
                    'users': list(data['users'].keys()),
                    'attempts': {user: count for user, count in data['users'].items()},
                    'timestamp': str(datetime.now())
                }
                send_kafka_alert(alert_data)
                
            ip_keys_to_remove.append(ip)

    # Remover IPs após a iteração para evitar erro
    for ip in ip_keys_to_remove:
        del attempts_by_ip[ip]

try:
    start_time = datetime.now()
    print(f"Buscando eventos a partir de: {start_time}")

    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                raise KafkaException(msg.error())

        log = msg.value().decode('utf-8')
        parsed_log = parse_log(log)
        
        if parsed_log:
            detect_brute_force(parsed_log)
        
        # Verificar se deve processar e enviar alertas
        current_time = datetime.now()
        if current_time - start_time >= INTERVAL:
            print(f"Buscando eventos a partir de: {current_time}")
            process_alerts()
            start_time = current_time

        # Aguardar um curto período antes da próxima iteração
        time.sleep(1)

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
