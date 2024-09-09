FROM confluentinc/cp-kafka-connect-base:4.0.0

RUN pip install --trusted-host pypi.python.org envtpl==0.6.0

ENV RABBITMQ_QUEUE="security"

COPY target /opt/target
COPY target/kafka-connect-target/usr/share/kafka-connect/kafka-connect-rabbitmq/* /usr/share/java/kafka/ 
COPY config-templates /opt/config-templates
COPY docker-entrypoint.sh /opt
RUN chmod +x /opt/docker-entrypoint.sh

WORKDIR /opt

CMD [ "./docker-entrypoint.sh" ]
