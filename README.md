Aqui está o README reformulado, com uma formatação mais atraente e estruturada:

---

# **Sn1tchAuth**  
*Aplicativo criado para a aula de Interoperabilidade 2*

## **💬 Acesse os Alertas**
Para visualizar os alertas, **cadastre-se no grupo do Telegram:**

🔗 [t.me/sn1tch_auth](https://t.me/sn1tch_auth)

---

## **🚀 Instalação no Amazon Linux**
1. [Crie uma instância com **Amazon Linux**.](https://docs.aws.amazon.com/pt_br/AWSEC2/latest/UserGuide/option3-task1-launch-ec2-instance.html)

---

## **📂 Clonar Repositório e Executar o Projeto**
```bash
git clone https://github.com/Sn1tchApp/interoperabilidade2.git
cd /path/to/repo
```

---

## **🔧 Instalar Make**
```bash
sudo yum install make
```

---

## **▶️ Primeira Execução**

### **🔨 Instalar e Inicializar Docker e Docker-Compose**
```bash
make install-docker

# Ou manualmente:
sudo yum install -y docker
sudo systemctl enable docker
sudo systemctl start docker
```
```bash
make install-docker-compose

# Ou manualmente:
curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

---

## **🌐 Criar Ambiente Completo**
Para criar o ambiente com todos os componentes de uma vez, execute:
```bash
make all
```

---

## **🔄 Criar o Ambiente Passo a Passo**

### **1️⃣ Criar Imagem Docker do Conector**
```bash
make build-connector

# Ou manualmente:
docker build -t connect ./connectors/kafka-connect-rabbitmq/
```

### **2️⃣ Criar Imagem do Docker Analyser**
```bash
make build-analyser

# Ou manualmente:
docker build -t analyser ./analyser
```

### **3️⃣ Habilitar MQTT no RabbitMQ**
```bash
make configure-mqtt

# Ou manualmente:
docker-compose up -d rabbitmq
sleep 30
docker exec -it interoperabilidade2-rabbitmq-1 rabbitmq-plugins enable rabbitmq_mqtt
docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqctl add_user guest guest
docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqctl add_user producer sn1tchapp
docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqctl set_permissions -p / guest ".*" ".*" ".*"
docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqctl set_permissions -p / producer ".*" ".*" ".*"
docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqadmin -u sn1tchapp -p sn1tchapp declare queue name=security durable=true
docker exec -it interoperabilidade2-rabbitmq-1 rabbitmqadmin -u sn1tchapp -p sn1tchapp declare binding source="amq.topic" destination_type="queue" destination="security" routing_key=security
```

### **4️⃣ Levantar Kafka e Criar Tópicos**
```bash
make configure-kafka

# Ou manualmente:
docker-compose up -d zookeeper kafka kafka-ui

# Criar os tópicos com a política correta (compact):
docker exec -it interoperabilidade2-kafka-1 kafka-topics --bootstrap-server localhost:9092 --create --topic connect-offsets --partitions 1 --replication-factor 1 --config cleanup.policy=compact
docker exec -it interoperabilidade2-kafka-1 kafka-topics --bootstrap-server localhost:9092 --create --topic connect-config --partitions 1 --replication-factor 1 --config cleanup.policy=compact
docker exec -it interoperabilidade2-kafka-1 kafka-topics --bootstrap-server localhost:9092 --create --topic connect-status --partitions 1 --replication-factor 1 --config cleanup.policy=compact
docker exec -it interoperabilidade2-kafka-1 kafka-topics --bootstrap-server localhost:9092 --create --topic security --partitions 1 --replication-factor 1 --config cleanup.policy=compact
```

### **5️⃣ Verificar se os Tópicos Foram Criados**
```bash
make check-topics-kafka

# Ou manualmente:
docker exec -it interoperabilidade2-kafka-1 kafka-topics --list --bootstrap-server localhost:9092
```

### **6️⃣ Iniciar os Demais Componentes**
```bash
make start-connect

# Ou manualmente:
docker-compose up -d connect analyser
```

---

## **📡 Coletar Logs de SSH**

No servidor onde deseja coletar os logs de SSH, siga os passos abaixo:

1. Navegue até a pasta `scripts` e abra o arquivo `log_coletor.py`.
2. Defina o **endereço do servidor MQTT** e o **caminho do arquivo de log a ser monitorado**, alterando as variáveis `MQTT_HOST` e `LOG_FILE`.
3. Execute o script:
```bash
python3 log_coletor.py
```
