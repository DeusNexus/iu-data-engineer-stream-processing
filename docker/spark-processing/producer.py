# producer.py
import time
from pyspark.sql import SparkSession
import random

def generate_random_number():
    while True:
        time.sleep(1)
        yield random.randint(1, 100)

if __name__ == "__main__":
    spark = SparkSession.builder.appName("RandomNumberProducer").getOrCreate()
    sc = spark.sparkContext

    rdd = sc.parallelize(generate_random_number())
    
    # Assuming you have a mechanism to send data to the master or a central system
    # This could be through a shared file system, a message queue, etc.
    # For the purpose of this example, we'll just print the number
    rdd.foreach(print)

    spark.stop()
