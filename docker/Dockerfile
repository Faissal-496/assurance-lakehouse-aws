# Spark Runtime Image - Lakehouse Project
# Spark 3.5.0 + S3A + Python deps

FROM apache/spark:3.5.0

# Root setup
USER root

ENV SPARK_HOME=/opt/spark
ENV HOME=/home/spark

ENV PATH=$SPARK_HOME/bin:/home/spark/.local/bin:$PATH

WORKDIR /opt/lakehouse

# System dependencies
RUN apt-get update && \
    apt-get install -y python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/

# Python dependencies (NO SECRETS)
COPY requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Jupyter kernel PySpark (REPRODUCTIBLE)
RUN python3 -m ipykernel install \
    --sys-prefix \
    --name pyspark \
    --display-name "PySpark (Spark 3.5)"

# S3 CONNECTORS
ADD https://repo.maven.apache.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar \
    /opt/spark/jars/

ADD https://repo.maven.apache.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar \
    /opt/spark/jars/

# Spark config + Ivy cache + PERMISSIONS (CRITICAL)
RUN mkdir -p /opt/spark/conf \
             /home/spark/.ivy2/cache \
             /home/spark/.ivy2/jars && \
    chown -R spark:spark /home/spark /opt/spark/conf /opt/spark/jars && \
    chmod -R 755 /opt/spark/jars && \
    echo "spark.jars.packages com.crealytics:spark-excel_2.12:3.5.1_0.20.4" \
    >> /opt/spark/conf/spark-defaults.conf

# Runtime user
USER spark

CMD ["sleep", "infinity"]
