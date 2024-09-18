#!/bin/bash

# This script installs and configures MySQL DB and Confluent Platform 7.7.0 on Ubuntu, including:
# - Starting MySQL, creating a user, and setting up the database
# - Starting Zookeeper, Kafka server, Schema Registry, and Kafka Connect services
# - Creating Kafka topics with Avro schemas
# - Configuring and deploying a Kafka Sink Connector to MySQL
# - Inserting a test entry into Kafka topics to validate the setup
# 
# At the end, the script provides instructions for:
# - Verifying data insertion in MySQL
# - Determining the IP address needed to connect to Kafka from Kafka producer and consumer clients

echo "Step 1: Update the system and install necessary dependencies"
sudo apt update -y
sudo apt upgrade -y
sudo apt install -y curl software-properties-common apt-transport-https openjdk-11-jdk

echo "Step 2: Install Confluent Platform"
curl -O http://packages.confluent.io/archive/7.7/confluent-community-7.7.0.tar.gz
tar -xzf confluent-community-7.7.0.tar.gz
export CONFLUENT_HOME=$HOME/confluent-7.7.0
export PATH=$CONFLUENT_HOME/bin:$PATH

echo "Step 3: Install MySQL"
sudo apt install -y mysql-server
sudo service mysql start

echo "Step 4: Configure MySQL"
sudo mysql -e "CREATE DATABASE kafka_db;"
sudo mysql -e "CREATE USER 'kafka_user'@'localhost' IDENTIFIED BY 'kafka_password';"
sudo mysql -e "GRANT ALL PRIVILEGES ON kafka_db.* TO 'kafka_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"
sudo mysql -e "USE kafka_db; CREATE TABLE processed_entries (disease VARCHAR(255), treatment VARCHAR(255));"

echo "Step 5: Set up Kafka Connect plugins: Downloading MySQL Connector and Kafka Connect JDBC JARs to /usr/share/java/kafka-connect-java as plugin.path in connect-distributed.properties refers to this path"
sudo mkdir -p /usr/share/java/kafka-connect-java
sudo curl -o /usr/share/java/kafka-connect-java/mysql-connector-java-8.0.13.jar https://repo.maven.apache.org/maven2/mysql/mysql-connector-java/8.0.13/mysql-connector-java-8.0.13.jar
sudo curl -o /usr/share/java/kafka-connect-java/kafka-connect-jdbc-10.4.0.jar https://packages.confluent.io/maven/io/confluent/kafka-connect-jdbc/10.4.0/kafka-connect-jdbc-10.4.0.jar

echo "Step 6: Updating Kafka server.properties configuration to expose the machine IP"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
CONFIG_FILE="$CONFLUENT_HOME/etc/kafka/server.properties"
echo "# Adding server socket use config" >> $CONFIG_FILE
echo "listeners=PLAINTEXT://0.0.0.0:9092" >> $CONFIG_FILE
echo "advertised.listeners=PLAINTEXT://$IP_ADDRESS:9092" >> $CONFIG_FILE

echo "Step 7: Start Zookeeper"
$CONFLUENT_HOME/bin/zookeeper-server-start $CONFLUENT_HOME/etc/kafka/zookeeper.properties > zookeeper.log 2>&1 &

echo "Step 8: Start Kafka Server"
$CONFLUENT_HOME/bin/kafka-server-start $CONFLUENT_HOME/etc/kafka/server.properties > kafka-server.log 2>&1 &

echo "Step 9: Start Schema Registry"
$CONFLUENT_HOME/bin/schema-registry-start $CONFLUENT_HOME/etc/schema-registry/schema-registry.properties > schema-registry.log 2>&1 &

echo "Step 10: Start Kafka Connect"
$CONFLUENT_HOME/bin/connect-distributed $CONFLUENT_HOME/etc/kafka/connect-distributed.properties > kafka-connect.log 2>&1 &

echo "Step 11: Sleep for 30 sec to let all service the time to lunch"
sleep 30

echo "Step 12: Create the 'processed-entries' Kafka topic"
$CONFLUENT_HOME/bin/kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic processed-entries

echo "Step 13: Register Avro schema for 'processed-entries' topic"
curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
    --data '{"schema": "{\"type\":\"record\",\"name\":\"ProcessedEntry\",\"fields\":[{\"name\":\"disease\",\"type\":\"string\"},{\"name\":\"treatment\",\"type\":\"string\"}]}"}' \
    http://localhost:8081/subjects/processed-entries-value/versions

echo "Step 14: Create the 'medical-entries' Kafka topic"
$CONFLUENT_HOME/bin/kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic medical-entries

echo "Step 15: Registering Avro schema for 'medical-entries' topic"
curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
    --data '{"schema": "{\"type\":\"record\",\"name\":\"MedicalThreatment\",\"fields\":[{\"name\":\"sentence_text\",\"type\":\"string\"},{\"name\":\"treatments\",\"type\":{\"type\":\"array\",\"items\":\"string\"}},{\"name\":\"query_metadata\",\"type\":{\"type\":\"map\",\"values\":\"string\"}}]}"}' \
    http://localhost:8081/subjects/medical-entries-value/versions


echo "Step 16: Configure Kafka MySQL Sink Connector"
cat <<EOF > mysql-sink-connector.json
{
  "name": "mysql-sink-connector",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "tasks.max": "1",
    "topics": "processed-entries",
    "connection.url": "jdbc:mysql://localhost:3306/kafka_db",
    "connection.user": "kafka_user",
    "connection.password": "kafka_password",
    "auto.create": "true",
    "insert.mode": "insert",
    "pk.mode": "none",
    "table.name.format": "processed_entries",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "io.confluent.connect.avro.AvroConverter",
    "value.converter.schema.registry.url": "http://localhost:8081"
  }
}
EOF

curl -X POST -H "Content-Type: application/json" --data @mysql-sink-connector.json http://localhost:8083/connectors

echo "Step 17: Publish a message to 'processed-entries' topic"
cat <<EOF > processed-entry.json
{"disease": "teratoma syndrome", "treatment": "Surgical resection"}
EOF

$CONFLUENT_HOME/bin/kafka-avro-console-producer \
  --broker-list localhost:9092 --topic processed-entries \
  --property value.schema='{"type":"record","name":"ProcessedEntry","fields":[{"name":"disease","type":"string"},{"name":"treatment","type":"string"}]}' < processed-entry.json

echo "Step 18: Verify Data Insertion into MySQL"
echo "------------------------------------------"
echo "1. Log in to MySQL with the following command:"
echo "   mysql -u kafka_user -p"
echo "2. When prompted, enter the password: kafka_password"
echo "3. Once logged in, switch to the correct database with this command:"
echo "   USE kafka_db;"
echo "4. Retrieve and display the inserted records by running this query:"
echo "   SELECT * FROM processed_entries;"
echo "------------------------------------------"
echo "Review the query output to confirm that the data has been successfully inserted into the 'processed_entries' table."
echo ""

echo "Step 19: Configure the Clients"
echo "Please update the Server IP address in the clients' configuration to: $IP_ADDRESS"