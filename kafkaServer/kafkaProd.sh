
#!/bin/sh
# Stop
docker stop "$1"
docker container rm "$1"
#PYTHON_APP=main2.py
#-ti --rm \ -v /dev/snd:/dev/snd \ --privileged \
docker build ../python/ --tag tap:python
docker run  --device /dev/snd:/dev/snd --network host -e PYTHON_APP=main2.py --name "$1" -it tap:python -e TZ=Europe/Rome
