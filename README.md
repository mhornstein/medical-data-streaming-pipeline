# Kafka Pipeline - Medical Text Mining

## Project Overview

This project simulates a real-time data pipeline using Apache Kafka, Python, Spacy, and MySQL. It models a scenario where medical entries about medical threatment are generated, processed to extract key information (illness and medicine), and then stored in MySQL.

## Architecture

The following diagram illustrates the architecture from both the business and implementation perspectives:

- **Picture placeholder**

## Platform

- **Kafka Consumers/Producer**: Run on Windows 10 with Python 3.10.8
- **Kafka Platform and MySQL**: Run on Ubuntu via WSL (Windows Subsystem for Linux)

## Installation

### 1. Install WSL 2 on Windows

1. **Download and Install WSL 2:**
   Follow the official [WSL installation guide](https://docs.microsoft.com/en-us/windows/wsl/install) to install WSL 2 on your Windows machine.

2. **Verify Installation:**
   - Open Command Prompt or PowerShell and run:
     ```bash
     wsl --list --verbose
     ```
   - If Ubuntu is not listed, install it by running:
     ```bash
     wsl --install -d Ubuntu
     ```
   - Set Ubuntu as the default distribution:
     ```bash
     wsl --set-default Ubuntu
     ```

3. **Start WSL:**
   Run `wsl` in Command Prompt or PowerShell to start the WSL environment.

### 2. Set Up MySQL DB and Confluent Platform on Ubuntu

This is done using the `setup_confluent_platform.sh` Script.
This script installs and configures MySQL DB and Confluent Platform 7.7.0 on Ubuntu, including:
- Starting MySQL, creating a user, and setting up the database.
- Starting Zookeeper, Kafka server, Schema Registry, and Kafka Connect services.
- Creating Kafka topics with Avro schemas.
- Configuring and deploying a Kafka Sink Connector to MySQL.
- Inserting a test entry into Kafka topics to validate the setup.

At the end, the script provides instructions for:
- Verifying data insertion in MySQL.
- Determining the IP address needed to connect to Kafka from Kafka producer and consumer clients.

1. **Create and Edit the Setup Script:**
   - Navigate to your home directory:
     ```bash
     cd ~
     ```
   - Create and edit the script `setup_confluent_platform.sh`:
     ```bash
     nano setup_confluent_platform.sh
     ```
   - Copy the content from the GitHub repository (`scripts\setup_confluent_platform.sh`) into the file.
   - Save and exit by pressing `Ctrl+X`, then `Y` to confirm, and `Enter` to exit.

2. **Make the Script Executable:**
   ```bash
   chmod +x setup_confluent_platform.sh
   ```

3. **Run the Script:**
   Start the services by running:
   ```bash
   ./setup_confluent_platform.sh
   ```
   Wait for the script to complete. At the end, the IP address of the server will be displayed.

### 3. Run Producer and Consumer on Windows

1. **Update Configuration:**
   - In `src/config.yaml`, update the `server_url` entry with the IP address provided by the script in the previous step. For example:
    `server_url: '172.28.60.217'`

2. **Run the Producer and Consumer:**
   - Execute the `start_kafka_producer_consumer.bat` script.

The producer will output the entries it produces, and the consumer will display the entries it consumes. Periodically check the MySQL table for updates.

- **output placeholder**