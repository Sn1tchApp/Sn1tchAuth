FROM python
RUN pip install requests confluent_kafka
WORKDIR /opt/
COPY . /opt/
ENTRYPOINT ["python3", "-u" ,"/opt/alert_brute_force.py"]