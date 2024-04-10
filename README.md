# IU INTERNATIONAL UNIVERSITY OF APPLIED SCIENCES

### Project: Data Engineering (DLBDSEDE02)
## Problem Statement
A municipality wants to measure environmental metrics by collecting data from sensors in the city.
While developing a solution the focus should be on a near real-time design that allows for quick response when environmental threshold values are exceeded and warn the citizens. The system, build for storage and processing, should also accommodate for scale, reliability and flexibility in case new sensors are installed with different continuous data streams.

## Approach
For the data source I will use simulated data streams which would offer greater test capabilities because we can customize the data to our liking and also adjust the frequency as we like. For the simulated sensor data a sample distribution will be used for each to get more realistic readings, additionally it would be possible to include incidental outliers and allow our system to detect them.

Each sensor would have the following data which can be send as JSON object: 
`sensor_id, temperature, humidity, pressure, air_quality, particulate_matter ,noise_level, illuminance, wind_speed, rainfall`

Apache Cassandra would be a great choice as database since it is proven to be scalable, fault tolerant, flexible and can handle high throughput with no single point of failure. Furthermore, CQL is SQL-like language easy to use and for city-wide sensor network the option for geographical distribution is perfect. Apache Spark seems to be the better choice than Kafka because it is better at performing complex analytics on real-time data streams and since the main goal is to provide alerts when thresholds exceed this would be more appropriate to alert citizens. Both of these technologies are proven to handle the requirements specified in the problem statement.

First the streaming data will be processed by Apache Spark calculating statistics, outliers can be detected triggering alerts (e.g. in API), the enriched sensor data can then be stored in Cassandra.
Periodic processing of batches can help to gain insight into long term developments.

# Development Planning - UML Schemas
## UML Diagram
Diagram -
![Design of ](/images/uml.jpg)

## Sensor Data Overview

The following sensors are augmented using random samples from their normal distributions while also using trend of last 300 readings.
Drift too far from the mean values is limited by using a simple recalibaration_rate set to 0.2
- temperature: μ=25 σ=2
- humidity: μ=60 σ=3
- pressure: μ=1013 σ=2
- air_quality: μ=200 σ=20
- particulate_matter: μ=30 σ=2
- noise_level: μ=50 σ=3
- illuminance: μ=500 σ=50
- wind_speed: μ=5 σ=20
- rainfall: μ=0 σ=3

![IoT Sensor Producers](/images/station_sensor_generation.gif)

The gif illustrates generations of the sensor data for different sensor stations. The iot stations will publish this data to the kafka topic to emulate real world sensor data collection.
One benefit is that the data frequency can easily be changed is unique and still follows an expected distributionn. Outliers will occur at times and we could calculate how often values below or above a certain percetile would occur.
In Spark Streaming the distributions are known for each sensor and we can therefor assess wether the received station readings are outlier or not and include it as enriched data when writing to Apache Cassandra for storage.

## Kafka
`docker push deusnexus/zookeeper`
`docker push deusnexus/broker`
`docker push deusnexus/client`
`docker push deusnexus/producer`
`docker push deusnexus/prometheus`
..

# Spark Streaming
`docker push deusnexus/spark-processing`

## Cassandra
`docker push deusnexus/cassandra`
..

# Docker Deploy Kafka
SELF NOTE: DONT USE VPN!!!!
1. Create a Docker Network using bridge
- `sudo docker network create -d bridge kafka-net`
1. Spin up zookeeper_jmx (the zookeeper orchestrates all the kafka brokers and is required) (Important to give it the name `zookeeper`)
- `sudo docker run -it --rm --name zookeeper --net kafka-net -p 2181:2181 -p 7071:7071 zookeeper_jmx`
2. Spin up brokers using broker_jmx (these will hold the topic(s) that are being received by consumers and broadcasted by producer)
- `sudo docker run --net kafka-net --rm --name broker-1 -p 9092:9092 -p 7072:7072 broker_jmx` => Consequent brokers can be called --name broker-2, broker-3 etc.
- `sudo docker exec -it -e KAFKA_OPTS="" broker-1 /bin/bash` Now we need to set KAFKA_OPTS="" otherwise we will get error!
- `/usr/local/kafka/bin/kafka-topics.sh --create --topic iot-sensor-stream --bootstrap-server broker-1:9092 --replication-factor 1 --partitions 3` Topic creation
- `exit`
3. Topic has been created for the brokers, the zookeeper propegates the topic to all running brokers. Now we need to publish sensor data to the kafka topic by spinning up the docker image `producer`
- `sudo docker run -it --rm --name producer-1 --net kafka-net kafka_producer`
4. Or alternatively can use docker-compose inside of the docker/kafka-producer folder. This will start N replicates as specified in the docker-compose.yml file.
- `sudo docker-compose up`
5. The topic is being populated now with new messages. To view the stream as a consumer do following (this assumes all the docker containers are on same network) and consumer is opened from local machine:
`./kafka-console-consumer.sh --bootstrap-server broker-1:9092 --topic iot-sensor-stream --from-beginning`


## Dashboards Metrics
Prometheus uses JMX to export metrics from Kafka to port 7071, 7072, 7072 (the zookeeper and each broker will have their own unique port that should be included in the prometheus config file.)
Prometheus: http://localhost:9090/graph?g0.expr=kafka_server_brokertopicmetrics_bytesin_total
Prometheus root dir: /usr/local/prometheus-2.50.1.linux-amd64
Prometheus Config File: /usr/local/prometheus-2.50.1.linux-amd64/prometheus.yml
Config File Example:
``
    # my global config
    global:
    scrape_interval: 2s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
    evaluation_interval: 2s # Evaluate rules every 15 seconds. The default is every 1 minute.
    # scrape_timeout is set to the global default (10s).

    # Alertmanager configuration
    alerting:
    alertmanagers:
        - static_configs:
            - targets:
            # - alertmanager:9093

    # Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
    rule_files:
    # - "first_rules.yml"
    # - "second_rules.yml"

    # A scrape configuration containing exactly one endpoint to scrape:
    # Here it's Prometheus itself.
    scrape_configs:
    # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
    - job_name: "kafka"

        # metrics_path defaults to '/metrics'
        # scheme defaults to 'http'.

        static_configs:
        - targets: ["localhost:7071","localhost:7072"]
``

Grafana: http://localhost:3000/dashboards

## Evaluation
..

## Reflection
..

# How to get started
## Dependencies
...
...

## Installation instructions
1. Download the Git repo using `git clone https://github.com/DeusNexus/iu-data-engineer-stream-processing`
2. Open folder using `cd iu-data-engineer-stream-processing` and create a new virtual environment using `python3 -m venv venv`.
3. Activate the virtual env using `source venv/bin/activate`. Now it should show (venv) in the terminal.
4. Now you can install the python modules using `pip install -r requirements.txt`
5. The working environment is now ready and you can run any script.

## API usage
...

# Reflection
- What I learned ...
- What challenges occured ...
- What recommendations are suggested ...
- What could be improved ...

# Conclusion
Did we achieve the goal etc and how?

# Disclaimer
The developed application is licensed under the GNU General Public License.