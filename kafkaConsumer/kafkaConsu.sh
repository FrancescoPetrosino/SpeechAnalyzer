# Stop
docker stop Consumer

# Remove previuos container 
docker container rm Consumer

docker build ../python/ --tag tap:python
docker run --network host -e PYTHON_APP=Consumer.py --name Consumer -it tap:python
