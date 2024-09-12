@echo off
rem Define the Kafka installation path (update it with your own definition)
set KAFKA_HOME=C:\kafka

echo Stopping Kafka broker...
call "%KAFKA_HOME%\bin\windows\kafka-server-stop.bat"

timeout /t 30 >nul 2>&1

echo Stopping ZooKeeper...
call "%KAFKA_HOME%\bin\windows\zookeeper-server-stop.bat"

timeout /t 30 >nul 2>&1

echo All services stopped.
pause