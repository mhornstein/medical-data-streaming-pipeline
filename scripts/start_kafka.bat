@echo off
rem Define the Kafka installation path (update it with your own definition)
set KAFKA_HOME=C:\kafka

echo Starting ZooKeeper...
start cmd /k "%KAFKA_HOME%\bin\windows\zookeeper-server-start.bat %KAFKA_HOME%\config\zookeeper.properties"

timeout /t 30 >nul 2>&1

echo Starting Kafka broker...
start cmd /k "%KAFKA_HOME%\bin\windows\kafka-server-start.bat %KAFKA_HOME%\config\server.properties"

timeout /t 30 >nul 2>&1

echo Creating Kafka topics...
call "%KAFKA_HOME%\bin\windows\kafka-topics.bat" --create --if-not-exists --topic medical-entries --bootstrap-server localhost:9092
call "%KAFKA_HOME%\bin\windows\kafka-topics.bat" --create --if-not-exists --topic processed-entries --bootstrap-server localhost:9092

echo All services started.
pause