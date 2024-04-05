# Build stage for downloading and extracting Kafka
FROM ubuntu:22.04 as builder

# Set environment variables to avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary tools for the build
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    wget \
    tar \
    && rm -rf /var/lib/apt/lists/*

# Define Kafka version and base URL for downloading
ENV KAFKA_VERSION=3.7.0
ENV KAFKA_BASE_URL=https://downloads.apache.org/kafka

# Download and extract Kafka
RUN wget ${KAFKA_BASE_URL}/${KAFKA_VERSION}/kafka_2.13-${KAFKA_VERSION}.tgz \
    && tar -xzf kafka_2.13-${KAFKA_VERSION}.tgz -C /tmp \
    && rm kafka_2.13-${KAFKA_VERSION}.tgz

# Move Kafka to the desired directory
RUN mv /tmp/kafka_2.13-${KAFKA_VERSION} /usr/local/kafka

# Final stage for running Kafka
FROM ubuntu:22.04

# Install Java Runtime and other necessary runtime tools
RUN apt-get update && apt-get install -y \
    iputils-ping \
    netcat \
    telnet \
    openjdk-11-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# Copy Kafka installation from the build stage
COPY --from=builder /usr/local/kafka /usr/local/kafka

# Set environment variables for Kafka
ENV KAFKA_HOME=/usr/local/kafka
ENV PATH="${KAFKA_HOME}/bin:${PATH}"

# Set the work directory and default command
WORKDIR /usr/local/kafka/bin
CMD ["kafka-topics.sh", "--create", "--topic", "iot-sensor-stream", "--bootstrap-server", "broker:9092", "--replication-factor", "1", "--partitions", "1"]
