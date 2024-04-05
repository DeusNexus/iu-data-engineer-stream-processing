# Building
cd docker/broker
sudo docker build -t broker .

## Run manual cassandra
sudo docker run -itd --name broker --network iotnet -p 9092:9092 -p 7072:7072 broker