#!/usr/bin/env bash
# Stop
docker stop kafkaServer

# Remove previuos container 
docker container rm kafkaServer

docker build ./ --tag tap:kafka
docker stop kafkaServer
docker run -e KAFKA_ACTION=start-kafka --network host -p 9092:9092 --name kafkaServer -it tap:kafka
