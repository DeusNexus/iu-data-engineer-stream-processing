## Building 
cd docker/prometheus
sudo docker build -t prometheus .

## Run manual prometheus
sudo docker run -itd --name prometheus --network iotnet -p 9090:9090 prometheus