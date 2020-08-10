# SpeechAnalyzer

### Progetto Technologies for Advanced Programming 2019/2020
- Aldo Fiorito X81000447
- Francesco Petrosino X81000533


### Setup 
- Clonare o scaricare il repository
- Setup Spark
    - Aggiungere il file [spark-2.4.5-bin-hadoop2.7.tgz][1] sulla directory spark/setup/


[1]: https://studentiunict-my.sharepoint.com/:f:/g/personal/uni389952_studium_unict_it/EtiOBtdaJKZMj9zeuzJJ9UcB60rLKQOOjFG6yk92CBy8JQ?e=YJqarn "Repository OneDrive"
- Setup Elastic

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
Inserire il proprio nome e la propria compagnia, infine selezionare la propria lingua

