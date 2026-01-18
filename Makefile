# Makefile pour lancer les scripts Spark
compose = docker compose -f docker/docker-compose.yml
SPARK_CONTAINER = lakehouse-spark
SCRIPT_PATH = /opt/lakehouse/lakehouse/lakehouse/ingestion/bronze_ingest.py
SCRIPT_GLUE_PATH = /opt/lakehouse/lakehouse/lakehouse/ingestion/bronze_ingest_with_glue.py

# -----------------------------
# Build / Up / Down et log
# -----------------------------
build:
	$(compose) build --no-cache
up:
	$(compose) up -d
down:
	$(compose) down
logs:
	$(compose) logs -f
# -----------------------------
# Lancer les scripts Spark
# -----------------------------
run-bronze:
	docker exec -it $(SPARK_CONTAINER) env PYTHONPATH=/opt/lakehouse/lakehouse spark-submit $(SCRIPT_PATH)
run-bronze-with-glue:
	docker exec -it $(SPARK_CONTAINER) env PYTHONPATH=/opt/lakehouse/lakehouse spark-submit $(SCRIPT_GLUE_PATH)
