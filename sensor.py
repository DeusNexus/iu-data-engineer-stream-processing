import time
import json
import random
import numpy as np

def generate_sensor_reading(sensor_id):
    timestamp = int(time.time())
    
    # Atmospheric Conditions
    temperature = np.random.normal(loc=25, scale=2)  # Simulate temperature with a normal distribution (mean=25, std=2)
    humidity = np.random.uniform(40, 60)  # Simulate humidity with a uniform distribution between 40 and 60
    pressure = np.random.normal(loc=1013, scale=5)  # Simulate atmospheric pressure with a normal distribution (mean=1013, std=5)
    
    # Air Quality
    air_quality = np.random.normal(loc=200, scale=20)  # Simulate air quality with a normal distribution (mean=200, std=20)
    particulate_matter = np.random.uniform(10, 50)  # Simulate particulate matter concentration with a uniform distribution between 10 and 50
    
    # Noise Level
    noise_level = np.random.uniform(30, 60)  # Simulate noise level with a uniform distribution between 30 and 60
    
    # Light Conditions
    illuminance = np.random.normal(loc=500, scale=50)  # Simulate illuminance with a normal distribution (mean=500, std=50)
    
    # Additional Environmental Factors
    wind_speed = np.random.uniform(0, 10)  # Simulate wind speed with a uniform distribution between 0 and 10
    rainfall = np.random.uniform(0, 5)  # Simulate rainfall with a uniform distribution between 0 and 5
    
    reading = {
        "timestamp": timestamp,
        "sensor_id": sensor_id,
        "temperature": round(temperature, 2),
        "humidity": round(humidity, 2),
        "pressure": round(pressure, 2),
        "air_quality": round(air_quality, 2),
        "particulate_matter": round(particulate_matter, 2),
        "noise_level": round(noise_level, 2),
        "illuminance": round(illuminance, 2),
        "wind_speed": round(wind_speed, 2),
        "rainfall": round(rainfall, 2)
    }

    return reading

def simulate_sensor_stream(sensor_id, interval_seconds=1, num_readings=10):
    for _ in range(num_readings):
        reading = generate_sensor_reading(sensor_id)
        print(json.dumps(reading))  # Print or send the reading to Kafka or any other streaming platform
        time.sleep(interval_seconds)

# Example usage:
simulate_sensor_stream(sensor_id="sensor_1", interval_seconds=1/10, num_readings=100)
