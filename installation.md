# Installation and Setup Guide for Confluent on Windows via WSL

## Environment Used

- **Windows Version:** 10
- **Python Version:** 3.10.8
- **Confluent Version:** 7.7.0

## Installation and Setup

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
   - Set Ubuntu to be the default option:
     ```bash
     wsl --set-default Ubuntu
     ```

3. **Start WSL:**
Run ```wsl``` in Command Prompt or PowerShell to start the WSL environment.

### 2. Prepare WSL Environment

1. **Update Package Lists:**
Run the following command to ensure your package lists are up-to-date:
     ```bash
     sudo apt update
     ```

2. **Install Java:**
Install OpenJDK 8 (required for Confluent):
     ```bash
     sudo apt install openjdk-8-jdk -y
     ```

3. **Navigate to Home Directory:**
Ensure you are in your home directory:
     ```bash
     cd ~
     ```

4. **Download and Extract Confluent Bundle:**
   - Download Confluent Community Bundle:
     ```bash
     curl -O https://packages.confluent.io/archive/7.7/confluent-community-7.7.0.tar.gz
     ```
   - Extract the bundle:
     ```bash
     tar xzf confluent-community-7.7.0.tar.gz
     ```

5. **Set Environment Variables:**
Add Confluent to your path by running:
     ```bash
     export CONFLUENT_HOME=~/confluent-7.7.0
     export PATH=$PATH:$CONFLUENT_HOME/bin
     ```

### 3.  Configuring Kafka to Work with WSL

1. **Find Out Your WSL IP Address**
   - Open your WSL terminal and run:
     ```bash
     ip a
     ```
   - Note the IP address assigned to `eth0`, typically shown under `inet`. For example: `172.28.60.217`.

2. **Update Kafka Configuration**
   - Open the `server.properties` file located in the `etc\kafka` directory of your Kafka installation.
   - Update the following properties:

     ```properties
     listeners=PLAINTEXT://0.0.0.0:9092
     advertised.listeners=PLAINTEXT://<your-ip>:9092
     ```

     Replace `<your-ip>` with the IP address you noted earlier. For example:

     ```properties
     listeners=PLAINTEXT://0.0.0.0:9092
     advertised.listeners=PLAINTEXT://172.28.60.217:9092
     ```

   - Save the changes.

### 4. Start Confluent Services
While you can use the Confluent CLI to manage services, in this guide, I used custom scripts to start the services.

1. **Create Start Script:**
Create a file named `start_kafka_confluent.sh`:
     ```bash
     touch start_kafka_confluent.sh
     ```

2. **Edit Script:**
   - Open the file for editing:
     ```bash
     nano start_kafka_confluent.sh
     ```
   - Paste the following script content:
     ```bash
     #!/bin/bash

     # Set the Confluent Home Directory (optional - in case not done manually)
     export CONFLUENT_HOME=~/confluent-7.7.0
     export PATH=$PATH:$CONFLUENT_HOME/bin

     start_zookeeper() {
       echo "Starting ZooKeeper..."
       $CONFLUENT_HOME/bin/zookeeper-server-start $CONFLUENT_HOME/etc/kafka/zookeeper.properties > zookeeper.log 2>&1 &
       sleep 5
       echo "ZooKeeper started."
     }

     start_kafka() {
       echo "Starting Kafka..."
       $CONFLUENT_HOME/bin/kafka-server-start $CONFLUENT_HOME/etc/kafka/server.properties > kafka.log 2>&1 &
       sleep 5
       echo "Kafka started."
     }

     start_schema_registry() {
       echo "Starting Schema Registry..."
       $CONFLUENT_HOME/bin/schema-registry-start $CONFLUENT_HOME/etc/schema-registry/schema-registry.properties > schema-registry.log 2>&1 &
       sleep 5
       echo "Schema Registry started."
     }

     start_kafka_connect() {
       echo "Starting Kafka Connect..."
       $CONFLUENT_HOME/bin/connect-distributed $CONFLUENT_HOME/etc/kafka/connect-distributed.properties > kafka-connect.log 2>&1 &
       sleep 5
       echo "Kafka Connect started."
     }

     create_topics() {
       echo "Creating Kafka topics..."
       $CONFLUENT_HOME/bin/kafka-topics --create --topic medical-entries --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
       $CONFLUENT_HOME/bin/kafka-topics --create --topic processed-entries --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
       echo "Topics created."
     }

     check_status() {
       echo "Checking status of services..."
       jps
     }

     # Start all services
     start_zookeeper
     start_kafka
     start_schema_registry
     start_kafka_connect

     # Wait for services to be fully up
     sleep 20

     # Create Kafka topics
     create_topics

     # Check the status of services
     check_status

     echo "All services started successfully."
     ```

3. **Save and Exit:**
   - Save the file by pressing `Ctrl+X`, then `Y` to confirm, and `Enter` to exit.

4. **Make Script Executable:**
Run:
     ```bash
     chmod +x start_kafka_confluent.sh
     ```

5. **Run the Script:**
Start the services by running:
     ```bash
     ./start_kafka_confluent.sh
     ```

### 5. Stop Confluent Services

To stop all services, simply shut down the WSL instance. This will terminate all running processes:
   ```bash
   wsl --terminate Ubuntu
   ```


To start it again, you can start your Ubuntu instance by running:
   ```bash
   wsl
   ```
   If you have multiple distributions and want to start a specific one, use:
   ```bash
   wsl -d Ubuntu
   ```

Please do not forget to update the new WSL ip in Kafka server as explained above for the new wsl instance.
 
## Additional References

- [Installing Confluent Platform](https://docs.confluent.io/platform/current/installation/installing_cp/zip-tar.html)
- [WSL Installation Guide](https://docs.microsoft.com/en-us/windows/wsl/install)
- [Installing Confluent on local machine YouTube Tutorial](https://www.youtube.com/watch?v=D5TSOt3hVTU)
