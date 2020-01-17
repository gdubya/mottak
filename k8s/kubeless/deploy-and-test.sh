#!/bin/bash
echo "Deleting existing function...."
kubeless function delete hello
echo "Deploying new function..."
kubeless function deploy hello --runtime python3.7 --from-file hello.py --handler test.hello
for i in 5 4 3 2 1; do
    kubeless function ls hello
    echo Waiting $i / $?
    sleep 1
done
echo "====== FUNCTION CALL ====="
kubeless function call hello --data "Hello there!"
echo "====== LOGS ======="
kubeless function logs hello
