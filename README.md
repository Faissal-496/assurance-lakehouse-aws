# Lakehouse ETL Pipeline

A data pipeline for processing large-scale insurance data using Apache Spark and AWS S3. Implements the medallion architecture (Bronze-Silver-Gold layers) with modular Python design.

## Quick Start

```bash
# Setup
export APP_ENV=dev
export S3_BUCKET=your-bucket-name

# Run pipeline
docker-compose up

# Or locally with make
make run-pipeline
```

## Architecture

Three-layer medallion pattern:

**Bronze** → Raw ingestion with schema validation  
**Silver** → Data consolidation and transformation  
**Gold** → Analytics tables ready for queries

## Setup

1. **Requirements**: Python 3.8+, Docker, AWS S3 credentials
2. **Configure**: Copy `.env.example` to `.env` and set your S3 bucket
3. **Run**: `make run-pipeline` or `docker-compose up`

## Configuration

YAML files in `config/`:
- `spark/` - Spark session settings
- `env/` - Environment-specific settings (dev/prod)
- `paths.yaml` - Data layer definitions

Priority: Environment variables > Specific YAML > Default YAML

## Project Structure

```
src/lakehouse/
├── main.py                  # Pipeline entry point
├── ingestion/               # Bronze layer (CSV → Parquet)
├── transformation/          # Silver & Gold transformations
├── quality/                 # Data validation
└── monitoring/              # Logging
```

## Requirements

- Python 3.8+
- Apache Spark 3.5.0
- Docker
- AWS S3 access

## Installation

### Using Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd assurance-lakehouse-aws

# Configure environment
export APP_ENV=dev
export S3_BUCKET=your-dev-bucket
export GLUE_DATABASE=your_dev_database

# Start the pipeline
docker-compose up
```

### Local Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export APP_ENV=dev
export S3_BUCKET=your-dev-bucket
export GLUE_DATABASE=your_dev_database
export DATA_BASE_PATH=/path/to/local/data

# Run pipeline
python3 -m lakehouse.main
```

## Usage

### Run Full Pipeline

```bash
# Using make
make run-pipeline

# Using Docker
docker-compose up

# Using Python directly
python3 -m lakehouse.main
```

### Run Individual Stages

```bash
# Bronze ingestion only
python3 run_bronze.py

# Silver transformation only
python3 run_silver.py

# Gold transformation only
python3 run_gold.py
```

### View Logs

```bash
# Docker logs
docker logs spark-lakehouse

# Filter for specific components
docker logs spark-lakehouse | grep -i "bronze\|silver\|gold"
```

## Configuration Examples

### Development Setup

```bash
export APP_ENV=dev
export S3_BUCKET=my-dev-bucket
export GLUE_DATABASE=my_dev_database
export SPARK_DRIVER_MEMORY=2g
export SPARK_EXECUTOR_MEMORY=2g

python3 -m lakehouse.main
```

### Production Setup

```bash
export APP_ENV=prod
export S3_BUCKET=my-prod-bucket
export GLUE_DATABASE=my_prod_database
export SPARK_DRIVER_MEMORY=8g
export SPARK_EXECUTOR_MEMORY=8g

python3 -m lakehouse.main
```

### Override Individual Settings

Environment variables override all YAML configurations:

```bash
export APP_ENV=prod
export SPARK_DRIVER_MEMORY=16g  # Override prod.yaml setting
python3 -m lakehouse.main
```

## Data Model

The pipeline processes large-scale insurance datasets with the following structure:

### Input Data
- Raw CSV files with various contract and client information
- Includes vehicle types, coverage details, and premium information

### Processing Steps
1. Schema validation and type enforcement
2. Contract data consolidation
3. Client profile enrichment
4. Premium aggregation and analysis

### Output Data
Three analytics-ready tables are created in the Gold layer with aggregations suitable for:
- Client profile analysis
- Contract analysis by type
- KPI dashboards for business metrics

## Code Quality

The codebase follows production standards:

- **Type hints**: All functions have type annotations
- **Error handling**: Comprehensive try-except blocks with logging
- **Logging**: Structured logging throughout with different levels
- **Documentation**: Docstrings on all modules and functions
- **Modular design**: Clear separation of concerns

## Monitoring and Logging

The pipeline provides detailed logging at each stage:

```
[2026-02-09 12:51:40,000] [INFO] STEP 1: BRONZE INGESTION
[2026-02-09 12:51:40,500] [INFO] Processing: contract_data.csv
[2026-02-09 12:51:41,000] [INFO] Bronze ingestion succeeded
[2026-02-09 12:51:41,500] [INFO] STEP 2: SILVER TRANSFORMATION
...
[2026-02-09 12:51:42,723] [INFO] LAKEHOUSE PIPELINE COMPLETED SUCCESSFULLY
```

## Troubleshooting

### S3 Bucket Not Found

Ensure environment variables are set correctly:
```bash
export S3_BUCKET=your-actual-bucket-name
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
```

### Out of Memory Errors

Increase Spark resources:
```bash
export SPARK_DRIVER_MEMORY=8g
export SPARK_EXECUTOR_MEMORY=8g
```

### Configuration Not Loading

Check that configuration files exist and are valid YAML:
```bash
ls -la config/spark/
ls -la config/env/
```

## Performance Considerations

- **Parallelism**: Adjust `spark.sql.shuffle.partitions` in config files
- **Memory**: Configure driver and executor memory based on data size
- **S3**: Use appropriate file format (Parquet is more efficient than CSV)
- **Network**: Ensure adequate bandwidth for data transfer

## Extending the Pipeline

### Adding a New Transformation

1. Create a new module in `src/lakehouse/transformation/`
2. Implement a `run(spark: SparkSession, resolver: PathResolver)` function
3. Import and call from `main.py`

### Adding Custom Configuration

1. Update YAML files in `config/` directory
2. Load configuration in your module using `config_loader.load_yaml()`
3. Environment variables can override YAML settings

### Adding Data Quality Checks

1. Define validation rules in `src/lakehouse/quality/`
2. Implement check functions with clear error messages
3. Call validation in transformation modules

## Testing

Validate the setup by running the pipeline in development mode:

```bash
export APP_ENV=dev
python3 -m lakehouse.main
```

Expected output includes successful completion of all three layers with data statistics.

## Environment Variables

Key environment variables used by the pipeline:

| Variable | Purpose | Example |
|----------|---------|---------|
| `APP_ENV` | Environment name | `dev` or `prod` |
| `S3_BUCKET` | S3 bucket name | `my-data-bucket` |
| `GLUE_DATABASE` | AWS Glue database | `my_analytics_db` |
| `DATA_BASE_PATH` | Local data directory | `/opt/lakehouse/data` |
| `SPARK_DRIVER_MEMORY` | Spark driver memory | `4g` |
| `SPARK_EXECUTOR_MEMORY` | Spark executor memory | `4g` |
| `SPARK_SHUFFLE_PARTS` | Shuffle partitions | `4` |
| `LOG_LEVEL` | Logging level | `INFO` or `WARN` |

## Support and Documentation

For detailed information see:
- [CONFIG_USAGE.md](CONFIG_USAGE.md) - Configuration guide
- [PIPELINE_GUIDE.md](PIPELINE_GUIDE.md) - Technical architecture and usage

## License

See [LICENSE](LICENSE) file for details.

## Contributing

When extending this pipeline:

1. Maintain the modular structure
2. Add comprehensive error handling
3. Include logging statements
4. Document configuration requirements
5. Update this README if adding major features

---

**Status**: Production Ready  
**Last Updated**: February 9, 2026  
**Spark Version**: 3.5.0
