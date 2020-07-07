#!/usr/bin/env bash
set -v
# Stop
docker stop kafkaTopic

# Remove previuos container 
docker container rm kafkaTopic

docker build ./ --tag tap:kafka
docker run -e KAFKA_ACTION=create-topic -e KAKFA_SERVER=127.0.0.1 -e KAFKA_TOPIC=$1 --network host --name kafkaTopic -it tap:kafka
