## Building 
cd docker/spark-processing
sudo docker build -t spark-processing .

## Run manual spark-processing
sudo docker run -itd --name spark-processing --network iotnet -p 7077:7077 spark-processing
