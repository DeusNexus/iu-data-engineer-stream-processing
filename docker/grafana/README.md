# Building
cd docker/grafana
sudo docker build -t grafana .

## Run manual grafana
sudo docker run -itd --name grafana --network host grafana