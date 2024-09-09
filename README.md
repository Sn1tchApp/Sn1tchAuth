# interoperabilidade2
Atividade da aula de interoperabilidade 2

## Instalar e inicializar docker e docker-compose

yum install -y docker

systemctl enable docker

systemctl start docker

curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose

chmod +x /usr/local/bin/docker-compose

## Clonar repositório e executar projeto

git clone https://github.com/Sn1tchApp/interoperabilidade2.git

cd /path/to/repo

## Criar imagem docker do conector

cd connectors/kafka-connect-rabbitmq/
docker build -t connect .

## Habilitar MQTT no rabbitmq

docker-compose up -d rabbitmq

'''
docker exec -it interoperabilidade2-rabbitmq-1 rabbitmq-plugins enable rabbitmq_mqtt

docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqctl add_user guest guest

docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqctl add_user producer sn1tchapp

docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqctl set_permissions -p / guest ".*" ".*" ".*"

docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqctl set_permissions -p / producer ".*" ".*" ".*"

docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqadmin -u sn1tchapp -p sn1tchapp declare queue name=security durable=true

docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqadmin -u sn1tchapp -p sn1tchapp declare binding source="amq.topic" destination_type="queue" destination="security" routing_key=security
'''

## Levantar kafka para criação dos tópicos necessários para o connector rabbitmq

docker-compose up -d zookeeper kafka kafka-ui

## Criar os tópicos com a política correta (compact)

docker exec -it interoperabilidade2-kafka-1 kafka-topics --bootstrap-server localhost:9092 --create --topic connect-offsets \
  --partitions 1 --replication-factor 1 \
  --config cleanup.policy=compact

docker exec -it interoperabilidade2-kafka-1 kafka-topics --bootstrap-server localhost:9092 --create --topic connect-config \
  --partitions 1 --replication-factor 1 \
  --config cleanup.policy=compact

docker exec -it interoperabilidade2-kafka-1 kafka-topics --bootstrap-server localhost:9092 --create --topic connect-status \
  --partitions 1 --replication-factor 1 \
  --config cleanup.policy=compact

docker exec -it interoperabilidade2-kafka-1 kafka-topics --bootstrap-server localhost:9092 --create --topic security \
  --partitions 1 --replication-factor 1 \
  --config cleanup.policy=compact

## Verifique se os tópicos estão criados

docker exec -it interoperabilidade2-kafka-1 kafka-topics --list --bootstrap-server localhost:9092

## Subir demais componentes do projeto

docker-compose up -d

## Executar coleta de log

procurar na pasta scripts o script log_coletor.py e definir o endereço do servidor mqtt e o endereço do arquivo de log a ser monitorado, alterando as variáveis MQTT_HOST, LOG_FILE .

python3 log_colector.py

## Comando para monitorar a fila MQTT na espera de mensagens

mosquitto_sub -h 18.231.148.22 -p 1883 -t "security" -u producer -P sn1tchapp
