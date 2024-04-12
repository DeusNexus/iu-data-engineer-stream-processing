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
Docker Architecture Diagram
![Design of ](/images/uml.jpg)

## Running the containers
Create the iotnet network which the docker containers can connect to:

`docker network create iotnet`

Terminal 1 - First start the Apache Cassandra Database (required for spark to connect to!):

`cd /docker/cassandra/docker-compose & docker-compose up`

Terminal 2 - Start the zookeeper, broker, prometheus and spark-processing:

`cd /docker & docker-compose up`

Terminal 3 - Now that Cassandra and Topic on broker is ready we can start publishing messages using producerse (these are the iot sensor stations creating readings):

`cd /docker/producer & docker-compose up`

Note that you can also change the number of producers in the docker-compose.yaml file if you wish to increase the load.

Terminal 4 - The messages should be published from the producers to the broker topic and then be read by the spark-processing pipeline to finally be written to Apache Cassandra Database.

You can also optionally start Grafana to view the metrics on dashboard (http://localhost:3001). Username: admin Password: admin

`cd /docker/grafana & docker-compose up`

It's also possible to run it as a daemon in background but you won't be able to see the console output.

**Docker Deployment with docker-compose (~28mb):**
![Docker Deployment with docker-compose (~28mb)](/images/docker_compose.gif)



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

**IoT Sensor Producers (~23mb):**
![IoT Sensor Producers (~23mb)](/images/station_sensor_generation.gif)


The gif illustrates generations of the sensor data for different sensor stations. The iot stations will publish this data to the kafka topic to emulate real world sensor data collection.
One benefit is that the data frequency can easily be changed is unique and still follows an expected distributionn. 

Outliers will occur at times and we could calculate how often values below or above a certain percetile would occur.
In Spark Streaming the distributions are known for each sensor and we can therefor assess whether the received station readings are outlier or not and include it as enriched data when writing to Apache Cassandra for storage.

## Apache Kafka
Images can be found here:
- https://hub.docker.com/repository/docker/deusnexus/zookeeper
- https://hub.docker.com/repository/docker/deusnexus/broker
- https://hub.docker.com/repository/docker/deusnexus/client
- https://hub.docker.com/repository/docker/deusnexus/producer
- https://hub.docker.com/repository/docker/deusnexus/prometheus

# Apache Spark Streaming
Docker Hub: https://hub.docker.com/repository/docker/deusnexus/spark-processing

## Apache Cassandra
Docker Hub: https://hub.docker.com/repository/docker/deusnexus/cassandra

Cassandra can run on iotnet or external (e.g. host) and has to run before spark-streaming is started.
- `cd /docker/cassandra & docker-compose up`

If you want to attach to it and use cqlsh for interacting with the database:
- `docker exec cassandra cqlsh`

SQL Commands:
- `USE iot_stations;`
- `SELECT * FROM spark_stream LIMIT 10;`

# Docker Deploy Kafka without docker-compose (individually)
Note: Don't use a VPN that blocks local intranet access.
1. Create a Docker Network using bridge
- `docker network create -d bridge iotnet`
1. Spin up zookeeper (the zookeeper orchestrates all the kafka brokers and is required) (Important to give it the name `zookeeper`)
- `docker run -it --rm --name zookeeper --net iotnet -p 2181:2181 -p 7071:7071 deusnexus/zookeeper`
2. Spin up brokers using broker (these will hold the topic(s) that are being received by consumers and broadcasted by producer)
- `docker run --net iotnet --rm --name broker-1 -p 9092:9092 -p 7072:7072 deusnexus/broker` => Consequent brokers can be called --name broker-2, broker-3 etc.
- `docker exec -it -e KAFKA_OPTS="" broker-1 /bin/bash` Now we need to set KAFKA_OPTS="" otherwise we will get error!
- `/usr/local/kafka/bin/kafka-topics.sh --create --topic iot-sensor-stream --bootstrap-server broker-1:9092 --replication-factor 1 --partitions 3` Topic creation
- `exit`
3. Topic has been created for the brokers, the zookeeper propegates the topic to all running brokers. Now we need to publish sensor data to the kafka topic by spinning up the docker image `producer`
- `docker run -it --rm --name producer-1 --net iotnet deusnexus/producer`
4. Or alternatively can use docker-compose inside of the docker/kafka-producer folder. This will start N replicates as specified in the docker-compose.yml file.
- `docker-compose up`
5. The topic is being populated now with new messages. To view the stream as a consumer do following (using the running zookeeper here as example):
- `docker exec -it zookeeper /bin/bash`
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
## Installation instructions
1. Download the Git repo using `git clone https://github.com/DeusNexus/iu-data-engineer-stream-processing`
2. Open folder using `cd iu-data-engineer-stream-processing` and create a new virtual environment using `python3 -m venv venv`.
3. Activate the virtual env using `source venv/bin/activate`. Now it should show (venv) in the terminal.
4. Now you can install the python modules using `pip install -r requirements.txt`
5. The working environment is now ready and you can run any script.

# Reflection
- What I learned ...
- What challenges occured ...
- What recommendations are suggested ...
- What could be improved ...

# Conclusion
Did we achieve the goal etc and how?

# Disclaimer
The developed application is licensed under the GNU General Public License.