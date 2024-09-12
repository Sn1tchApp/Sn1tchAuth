# Interoperabilidade2
Atividade da aula de interoperabilidade 2

## Para visualizar os alertas se cadastrar no grupo do Telegram

t.me/sn1tch_auth

## Instalar em um amazon linux

Criar máquina amazon linux

## Clonar repositório e executar projeto

git clone https://github.com/Sn1tchApp/interoperabilidade2.git

cd /path/to/repo

## Instalar Make

sudo yum install make

## Executar a primeira vez

### Instalar e inicializar docker e docker-compose

make install-docker

    yum install -y docker

    systemctl enable docker

    systemctl start docker

make install-docker-compose

    curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose

    chmod +x /usr/local/bin/docker-compose


## Criar ambiente de uma vez

make all

## Caso tenha interesse de criar passo a passo, executar a sequencia abaixo

### 1 - Criar imagem docker do conector

make build-connector

	docker build -t connect ./connectors/kafka-connect-rabbitmq/

### 2 - Criar imagem do docker analyser

make build-analyser

    docker build -t analyser ./analyser

### 3 - Habilitar MQTT no rabbitmq

make configure-mqtt

    docker-compose up -d rabbitmq
	sleep 30
	docker exec -it interoperabilidade2-rabbitmq-1 rabbitmq-plugins enable rabbitmq_mqtt
	docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqctl add_user guest guest
	docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqctl add_user producer sn1tchapp
	docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqctl set_permissions -p / guest ".*" ".*" ".*"
	docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqctl set_permissions -p / producer ".*" ".*" ".*"
	docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqadmin -u sn1tchapp -p sn1tchapp declare queue name=security durable=true
	docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqadmin -u sn1tchapp -p sn1tchapp declare binding source="amq.topic" destination_type="queue" destination="security" routing_key=security

### 4 - Levantar kafka para criação dos tópicos necessários para o connector rabbitmq

make configure-kafka

    docker-compose up -d zookeeper kafka kafka-ui

    ## Criar os tópicos com a política correta (compact)

    docker exec -it interoperabilidade2-kafka-1 kafka-topics --bootstrap-server localhost:9092 --create --topic connect-offsets --partitions 1 -replication-factor 1 --config cleanup.policy=compact

    docker exec -it interoperabilidade2-kafka-1 kafka-topics --bootstrap-server localhost:9092 --create --topic connect-config --partitions 1 --replication-factor 1 --config cleanup.policy=compact

    docker exec -it interoperabilidade2-kafka-1 kafka-topics --bootstrap-server localhost:9092 --create --topic connect-status --partitions 1 --replication-factor 1 --config cleanup.policy=compact

    docker exec -it interoperabilidade2-kafka-1 kafka-topics --bootstrap-server localhost:9092 --create --topic security --partitions 1 --replication-factor 1 --config cleanup.policy=compact


### 5 - Verifique se os tópicos estão criados

make check-topics-kafka

    docker exec -it interoperabilidade2-kafka-1 kafka-topics --list --bootstrap-server localhost:9092

### 6 - Subir demais componentes do projeto

make start-connect

    docker-compose up -d connect analyser


## No servidor que deseja coletar o log de ssh

### Executar coleta de log no servidor para analisar os logs de ssh

procurar na pasta scripts o script log_coletor.py e definir o endereço do servidor mqtt e o endereço do arquivo de log a ser monitorado, alterando as variáveis MQTT_HOST, LOG_FILE .

python3 log_colector.py
