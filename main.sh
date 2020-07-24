#Install py requirements
echo "Installo le componenti essenziali.."

echo "[1/] Installo pip..\n"
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python2.7 get-pip.py
rm get-pip.py

echo "[2/] Installo pulseaudio..\n"
sudo install pulseaudio
sudo killall pulseaudio
pulseaudio --start

echo "[3/] Installo portaudio..\n"
sudo apt install python-dev
sudo apt install portaudio19-dev

echo "[4/] Installo SpeechRecognition..\n"
python2.7 -m pip install SpeechRecognition

echo "[5/] Installo PyAudio..\n"
python2.7 -m pip install PyAudio

echo "[6/] Installo Kafka-Python..\n"
python2.7 -m pip install kafka-python


# Run main.py
#./python/bin/main.py
 