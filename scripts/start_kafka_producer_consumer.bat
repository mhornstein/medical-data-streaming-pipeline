@echo off
REM Change directory to the location of producer.py and run it
start cmd /k "cd /d .. && python producer.py"

REM Change directory to the location of consumer.py and run it
start cmd /k "cd /d .. && python consumer.py"

exit