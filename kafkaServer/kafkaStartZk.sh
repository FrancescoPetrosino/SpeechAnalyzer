#!/usr/bin/env bash
# Stop
docker stop kafkaZK

# Remove previuos container 
docker container rm kafkaZK

docker build ./ --tag tap:kafka
docker run -e KAFKA_ACTION=start-zk --network host -p 2181:2181 --name kafkaZK -it tap:kafka
