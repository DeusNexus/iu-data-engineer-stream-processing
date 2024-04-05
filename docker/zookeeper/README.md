# Kafka Zookeeper
sudo docker build -t zookeeper_jmx .

## Run zookeeper
sudo docker run -p 2181:2181 -p 5555:5555 -d zookeeper_jmx
