cd docker/kafka-producer
sudo docker build -t kafka-producer .
sudo docker run --network="host" kafka-producer
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic sensor-data --from-beginning