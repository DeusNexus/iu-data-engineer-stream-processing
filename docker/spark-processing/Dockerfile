# Use a multi-stage build to keep only what's necessary
# Stage 1: Build stage for downloading and unpacking Spark
FROM openjdk:8-jdk-slim as builder

# Install only the necessary dependencies
RUN apt-get update && \
    apt-get install -y wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

# Download and unpack Spark, then remove the tar file to save space
RUN wget --no-verbose "https://dlcdn.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3-scala2.13.tgz" && \
    tar -xzf spark-3.5.1-bin-hadoop3-scala2.13.tgz && \
    rm spark-3.5.1-bin-hadoop3-scala2.13.tgz

# Stage 2: Final stage to setup the Spark environment
FROM openjdk:8-jre-slim

# Copy the Spark installation from the builder stage
COPY --from=builder /tmp/spark-3.5.1-bin-hadoop3-scala2.13 /opt/spark

# Set environment variables
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin

# Install Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the producer script into the container
COPY producer.py /producer.py

# Start the producer script
CMD ["spark-submit", "/producer.py"]
