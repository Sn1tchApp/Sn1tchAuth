# Como executar em conteiner
docker build -t port_attack_simul .
docker run --rm -it --network host port_attack_simul

** a chave "port_attack_simul" pode se refere ao nome da imagem do docker e pode ser alterada, o importante é usar o mesmo no build e no run**