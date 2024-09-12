@echo off
rem Define the Kafka installation path (update it with your own definition)
set KAFKA_HOME=C:\kafka

echo Starting ZooKeeper...
start cmd /k "%KAFKA_HOME%\bin\windows\zookeeper-server-start.bat %KAFKA_HOME%\config\zookeeper.properties"

timeout /t 30 >nul 2>&1

echo Starting Kafka broker...
start cmd /k "%KAFKA_HOME%\bin\windows\kafka-server-start.bat %KAFKA_HOME%\config\server.properties"

echo All services started.
pause