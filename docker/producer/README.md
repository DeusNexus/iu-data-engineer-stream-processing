cd docker/kafka-producer
sudo docker build -t kafka-producer .
sudo docker run --network="host" kafka-producer
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic sensor-data --from-beginning

sudo docker-compose up -d # Run X containers as specified in docker-compose.yml
sudo docker stop $(sudo docker ps -q) # Stop all containers
sudo docker rm -f $(sudo docker ps -aq) # Remove all unused docker container labels
