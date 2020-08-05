FROM openjdk:8-jre

ENV PATH $SPARK_DIR/bin:$PATH
ENV SPARK_VERSION=2.4.5
ENV SPARK_DIR=/opt/spark
ENV PATH $SPARK_DIR/bin:$PATH

ADD ./setup/spark-${SPARK_VERSION}-bin-hadoop2.7.tgz /opt

RUN apt-get update && apt-get -y install bash python python-pip


RUN pip install pyspark
RUN pip install pytz
RUN pip install numpy 
RUN pip install elasticsearch
RUN pip install pandas

# Create Sym Link 
RUN ln -s /opt/spark-${SPARK_VERSION}-bin-hadoop2.7 ${SPARK_DIR} 
#ADD ./dataset/* /opt/tap/dataset
ADD ./code/*  /opt/tap/
ADD ./spark-manager.sh $SPARK_DIR/bin/spark-manager
ADD ./user.txt /opt/tap/

WORKDIR ${SPARK_DIR}
ENTRYPOINT [ "spark-manager" ]
