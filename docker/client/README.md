# Building
cd docker/client
sudo docker build -t client .

## Run manual client
sudo docker run -itd --name client --network iotnet client