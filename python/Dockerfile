FROM python:3
ENV PATH /usr/src/app/bin:$PATH
WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt-get update

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install SpeechRecognition
RUN pip install pytz
RUN apt-get install -y portaudio19-dev
RUN pip install PyAudio
RUN apt-get install -y pulseaudio
RUN apt-get install -y alsa-utils
RUN apt-get install alsa-source


COPY bin/* ./
COPY python-manager.sh /
ENTRYPOINT [ "/python-manager.sh" ]
