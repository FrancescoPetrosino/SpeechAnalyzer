FROM python:3
ENV PATH /usr/src/app/bin:$PATH
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install speechrecognition
RUN pip install pytz
RUN apt-get update
RUN apt-get install -y portaudio19-dev
RUN apt-get update
RUN pip install pyaudio
RUN apt-get update


COPY bin/* ./
COPY python-manager.sh /
ENTRYPOINT [ "/python-manager.sh" ]
