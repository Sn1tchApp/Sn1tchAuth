install-docker:
	yum install -y docker
	systemctl enable docker
	systemctl start docker

install-docker-compose:
	curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
	chmod +x /usr/local/bin/docker-compose

build-connector:
	docker build -t connect ./connectors/kafka-connect-rabbitmq/

build-analyser:
	docker build -t analyser ./analyser

configure-mqtt:
	docker-compose up -d rabbitmq
	sleep 30
	docker exec -it interoperabilidade2-rabbitmq-1 rabbitmq-plugins enable rabbitmq_mqtt
	docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqctl add_user guest guest
	docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqctl add_user producer sn1tchapp
	docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqctl set_permissions -p / guest ".*" ".*" ".*"
	docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqctl set_permissions -p / producer ".*" ".*" ".*"
	docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqadmin -u sn1tchapp -p sn1tchapp declare queue name=security durable=true
	docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqadmin -u sn1tchapp -p sn1tchapp declare binding source="amq.topic" destination_type="queue" destination="security" routing_key=security

configure-kafka:
	docker-compose up -d zookeeper kafka kafka-ui
	docker exec -it interoperabilidade2-kafka-1 kafka-topics --bootstrap-server localhost:9092 --create --topic connect-offsets --partitions 1 -replication-factor 1 --config cleanup.policy=compact
	docker exec -it interoperabilidade2-kafka-1 kafka-topics --bootstrap-server localhost:9092 --create --topic connect-config --partitions 1 --replication-factor 1 --config cleanup.policy=compact
	docker exec -it interoperabilidade2-kafka-1 kafka-topics --bootstrap-server localhost:9092 --create --topic connect-status --partitions 1 --replication-factor 1 --config cleanup.policy=compact
	docker exec -it interoperabilidade2-kafka-1 kafka-topics --bootstrap-server localhost:9092 --create --topic security --partitions 1 --replication-factor 1 --config cleanup.policy=compact

check-topics-kafka:
	docker exec -it interoperabilidade2-kafka-1 kafka-topics --list --bootstrap-server localhost:9092

start-connect:
	docker-compose up -d connect analyser

test-password-spray:
	python3 scripts/testes/test_password_spray.py

test-brute-force:
	python3 scripts/testes/test_brute_force.py

test-log-generate:
	python3 scripts/testes/test_simula_geracao.py

send-logs:
	python3 coletor/log_colector.py

all:
	make build-connector
	make build-analyser
	make configure-mqtt
	make configure-kafka
	make check-topics-kafka
	make start-connect



