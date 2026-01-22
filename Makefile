# Makefile pour lancer les scripts Spark
compose = docker compose -f docker/docker-compose.yml
SPARK_CONTAINER = spark-lakehouse
SCRIPT_PATH = /opt/lakehouse/lakehouse/lakehouse/ingestion/bronze_ingest.py
SCRIPT_GLUE_PATH = /opt/lakehouse/lakehouse/lakehouse/ingestion/bronze_ingest_with_glue.py

# Build / Up / Down et log
build:
	$(compose) build --no-cache
up:
	$(compose) up -d
down:
	$(compose) down
logs:
	$(compose) logs -f
# Lancer les scripts Spark
run-bronze:
	docker exec -it $(SPARK_CONTAINER) env PYTHONPATH=/opt/lakehouse/lakehouse spark-submit $(SCRIPT_PATH)
run-bronze-with-glue:
	docker exec -it $(SPARK_CONTAINER) env PYTHONPATH=/opt/lakehouse/lakehouse spark-submit $(SCRIPT_GLUE_PATH)
run-spak-bash:
	docker exec -it $(SPARK_CONTAINER) bash

run-jupyter-lab:

	docker exec -it \
  -w /home/spark \
  -e PYSPARK_DRIVER_PYTHON=jupyter \
  -e PYSPARK_DRIVER_PYTHON_OPTS="lab --ip=0.0.0.0 --no-browser --allow-root" \
  $(SPARK_CONTAINER) \
  pyspark

run-silver:
	docker exec -it $(SPARK_CONTAINER) env PYTHONPATH=/opt/lakehouse/lakehouse spark-submit /opt/lakehouse/lakehouse/lakehouse/transformation/bronze_to_silver.py

run-gold:
	docker exec -it $(SPARK_CONTAINER) env PYTHONPATH=/opt/lakehouse/lakehouse spark-submit /opt/lakehouse/lakehouse/lakehouse/transformation/silver_to_gold.py

run-main:
	docker exec -it $(SPARK_CONTAINER) env PYTHONPATH=/opt/lakehouse/lakehouse spark-submit /opt/lakehouse/lakehouse/lakehouse/main.py