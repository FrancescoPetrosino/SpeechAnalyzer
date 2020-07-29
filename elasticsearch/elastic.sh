#!/usr/bin/env bash
# Stop
docker stop elasticsearch

# Remove previuos container 
docker container rm elasticsearch

# Build
docker build ./ --tag tap:elasticsearch

docker run -t  -p 9200:9200 -p 9300:9300  --name elasticsearch -v /es-volume --mount source=es-volume,destination=/usr/share/elasticsearch/data --network host -e "discovery.type=single-node"  tap:elasticsearch
