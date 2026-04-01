# Makefile - Lakehouse Pipeline Commands
compose = docker compose -f docker/docker-compose.yml
SPARK_CONTAINER = spark-lakehouse
PYTHON_PATH = /opt/lakehouse/src

# Container management
build:
	$(compose) build --no-cache

up:
	$(compose) up -d

down:
	$(compose) down

logs:
	$(compose) logs -f

shell:
	docker exec -it $(SPARK_CONTAINER) bash

# Spark-submit commands (correct paths)
run-bronze:
	docker exec -it $(SPARK_CONTAINER) env PYTHONPATH=$(PYTHON_PATH) \
	spark-submit /opt/lakehouse/src/lakehouse/ingestion/bronze_ingest.py

run-silver:
	docker exec -it $(SPARK_CONTAINER) env PYTHONPATH=$(PYTHON_PATH) \
	spark-submit /opt/lakehouse/src/lakehouse/transformation/bronze_to_silver.py

run-gold:
	docker exec -it $(SPARK_CONTAINER) env PYTHONPATH=$(PYTHON_PATH) \
	spark-submit /opt/lakehouse/src/lakehouse/transformation/silver_to_gold.py

# Complete pipeline (recommended)
run-pipeline:
	docker exec -it $(SPARK_CONTAINER) env PYTHONPATH=$(PYTHON_PATH) \
	spark-submit /opt/lakehouse/src/lakehouse/main.py

# Jupyter Lab for interactive development
run-jupyter:
	docker exec -it \
  -w /home/spark \
  -e PYSPARK_DRIVER_PYTHON=jupyter \
  -e PYSPARK_DRIVER_PYTHON_OPTS="lab --ip=0.0.0.0 --no-browser --allow-root" \
  $(SPARK_CONTAINER) \
  pyspark

# Development helpers
test-imports:
	docker exec -it $(SPARK_CONTAINER) env PYTHONPATH=$(PYTHON_PATH) \
	python3 -c "from lakehouse.paths import PathResolver; print('Imports OK')"

info:
	@echo "=== Lakehouse Pipeline ==="
	@echo "Available commands:"
	@echo "  make build          - Build Docker image"
	@echo "  make up             - Start containers"
	@echo "  make down           - Stop containers"
	@echo "  make logs           - View container logs"
	@echo "  make shell          - Open Spark container shell"
	@echo ""
	@echo "Pipeline execution:"
	@echo "  make run-bronze     - Run bronze ingestion"
	@echo "  make run-silver     - Run silver transformation"
	@echo "  make run-gold       - Run gold transformation"
	@echo "  make run-pipeline   - Run complete ETL pipeline"
	@echo ""
	@echo "Development:"
	@echo "  make run-jupyter    - Launch Jupyter Lab"
	@echo "  make test-imports   - Verify Python imports"
	@echo ""
