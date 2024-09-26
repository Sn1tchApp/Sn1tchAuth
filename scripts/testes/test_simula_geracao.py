import random
import time

# Define o caminho do arquivo de log
log_file_path = "/tmp/security.log"

# Lista de endereços IP para simular acessos
ip_addresses = [
    "192.168.1.10", "172.16.0.5", "10.0.0.1", "172.24.0.69", "203.0.113.15"
]

# Usuários comuns para tentativas de login
usernames = ["julio", "maria", "joao", "ana", "pedro"]

# Lista de servidores para simular acessos
servers = ["GUSOLA-02", "SERVER-01", "HOST-03", "PROD-DB", "TEST-SRV"]

# Função para gerar um evento de log SSH
def generate_ssh_log():
    server = random.choice(servers)
    ip_address = random.choice(ip_addresses)
    port = random.randint(1024, 65535)
    username = random.choice(usernames)
    
    # Probabilidade de falha ou sucesso
    if random.random() < 0.7:  # 70% de chance de falha
        log_line = f"{server} sshd[{random.randint(10000, 30000)}]: Failed password for {username} from {ip_address} port {port} ssh2\n"
    else:  # 30% de chance de sucesso
        log_line = f"{server} sshd[{random.randint(10000, 30000)}]: Accepted password for {username} from {ip_address} port {port} ssh2\n"

    return log_line

# Função principal para escrever logs continuamente
def simulate_logs():
    with open(log_file_path, "a") as log_file:
        while True:
            log_event = generate_ssh_log()
            log_file.write(log_event)
            log_file.flush()  # Garante que o log seja gravado imediatamente no arquivo
            time.sleep(random.uniform(0.5, 2))  # Espera aleatória entre 0.5 a 2 segundos

if __name__ == "__main__":
    print(f"Simulação de logs SSH iniciada. Logs sendo gravados em {log_file_path}")
    simulate_logs()
