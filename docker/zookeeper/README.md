## Building 
cd docker/zookeeper
sudo docker build -t zookeeper .

## Run manual zookeeper
sudo docker run -itd --name zookeeper --network iotnet -p 2181:2181 -p 5555:5555 zookeeper
