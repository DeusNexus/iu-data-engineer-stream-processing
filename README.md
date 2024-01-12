# IU INTERNATIONAL UNIVERSITY OF APPLIED SCIENCES

### Project: Data Engineering (DLBDSEDE02)
## Problem Statement
A municipality wants to measure environmental metrics by collecting data from sensors in the city.
While developing a solution the focus should be on a near real-time design that allows for quick response when environmental threshold values are exceeded and warn the citizens. The system, build for storage and processing, should also accommodate for scale, reliability and flexibility in case new sensors are installed with different continuous data streams.

## Approach
For the data source I will use simulated data streams which would offer greater test capabilities because we can customize the data to our liking and also adjust the frequency as we like. For the simulated sensor data a sample distribution will be used for each to get more realistic readings, additionally it would be possible to include incidental outliers and allow our system to detect them.

Each sensor would have the following data which can be send as JSON object: sensor_id, temperature, humidity, pressure, air_quality, particulate_matter ,noise_level, illuminance, wind_speed, rainfall.

Apache Cassandra would be a great choice as database since it is proven to be scalable, fault tolerant, flexible and can handle high throughput with no single point of failure. Furthermore, CQL is SQL-like language easy to use and for city-wide sensor network the option for geographical distribution is perfect. Apache Spark seems to be the better choice than Kafka because it is better at performing complex analytics on real-time data streams and since the main goal is to provide alerts when thresholds exceed this would be more appropriate to alert citizens. Both of these technologies are proven to handle the requirements specified in the problem statement.

First the streaming data will be processed by Apache Spark calculating statistics, outliers can be detected triggering alerts (e.g. in API), the enriched sensor data can then be stored in Cassandra.
Periodic processing of batches can help to gain insight into long term developments.

# Development Planning - UML Schemas
## UML Diagram
Diagram -
![Design of ](/images/UML.jpg)

## Sensor Data Overview
JSON model, sample distribution, velocity

## Kafka
..

## Cassandra
..

## Evaluation
..

## Reflection
..

# How to get started
## Dependencies
...
...

## Installation instructions
...

## API usage
...

# Reflection
What I learned ...
What challenges occured ...
What recommendations are suggested ...
What could be improved ...

# Conclusion
Did we achieve the goal etc and how?

# Disclaimer
The developed application is licensed under the GNU General Public License.