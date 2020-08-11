# SpeechAnalyzer

### Progetto Technologies for Advanced Programming 2019/2020
- Aldo Fiorito X81000447
- Francesco Petrosino X81000533


### Setup 
- Clonare o scaricare il repository
- Setup Spark
    - Aggiungere il file [spark-2.4.5-bin-hadoop2.7.tgz][1] sulla directory spark/setup/
- Setup Elastic
    - Aggiungere il file [elasticsearch-hadoop-7.8.0.jar][2] sulla directory spark/setup/
Assicurarsi di avere [Docker][3]    

### Guida per l'utilizzo
**N.B Tutti i comandi devono essere lanciati in terminali differenti**
- Spostarsi sulla cartella "kafkaServer"
    - ./kafkaStartZk.sh
    - ./kafkaStartServer.sh
- Spostarsi in "elasticsearch"
    - ./elastic.sh
- Andare in "spark"
    - ./startSpark.sh
- Come ultima cartella andare su "kibana"
    - ./kibana.sh

Aprire una nuova console di comando e spostarsi nella root di  "SpeechAnalyzer" 
e lanciare il comando : "python3 form.py"
Inserire il proprio nome e la propria compagnia, infine selezionare la propria lingua e registrarsi.

[1]: https://studentiunict-my.sharepoint.com/:f:/g/personal/uni389952_studium_unict_it/EtiOBtdaJKZMj9zeuzJJ9UcB60rLKQOOjFG6yk92CBy8JQ?e=YJqarn "Repository OneDrive sp"
[2]: https://studentiunict-my.sharepoint.com/:u:/g/personal/uni389952_studium_unict_it/EeNAcubCzxxOpPPCLQOAznABSBqiCYsNhG7ZTEXAaENepg?e=jsPF6m "Repository OneDrive es"
[3]:https://docs.docker.com/get-docker/ "Docker"