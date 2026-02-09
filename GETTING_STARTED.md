# Getting Started

## Prerequisites

- Python 3.8+, Docker, AWS S3 access
- 4GB memory minimum

## Setup

1. **Clone and prepare**
```bash
git clone <repo>
cd assurance-lakehouse-aws
cp .env.example .env
```

2. **Configure** (edit `.env`)
```
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
S3_BUCKET=your_bucket
APP_ENV=dev
```

3. **Run**
```bash
# Docker (recommended)
docker-compose up

# Or with Make
make run-pipeline
```

## Configuration

Update `config/env/dev.yaml` (or prod.yaml) with your S3 bucket and environment settings.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| S3_BUCKET not set | `export S3_BUCKET=your-bucket` |
| Out of memory | Increase `SPARK_DRIVER_MEMORY` in .env |
| Docker fails | Run `docker-compose build --no-cache` |
| ImportError pyspark | Use Docker: `docker-compose up` |
| `SPARK_EXECUTOR_MEMORY` | Executor memory | `2g` or `4g` |

See [CONFIG_USAGE.md](CONFIG_USAGE.md) for complete configuration guide.

## Common Workflows

### Running in Development

```bash
export APP_ENV=dev
export S3_BUCKET=my-dev-bucket
make run-pipeline
```

### Running in Production

```bash
export APP_ENV=prod
export S3_BUCKET=my-prod-bucket
export SPARK_DRIVER_MEMORY=8g
make run-pipeline
```

### Running Individual Stages

```bash
# Bronze only
python3 run_bronze.py

# Silver only
python3 run_silver.py

# Gold only
python3 run_gold.py
```

### Checking Logs

```bash
# Docker logs
docker logs spark-lakehouse

# Filter by stage
docker logs spark-lakehouse | grep -i silver

# Follow logs
docker logs -f spark-lakehouse
```

## Next Steps

1. Read [README.md](README.md) for project overview
2. Review [PIPELINE_GUIDE.md](PIPELINE_GUIDE.md) for technical details
3. Check [CONFIG_USAGE.md](CONFIG_USAGE.md) for configuration options
4. Explore the `src/lakehouse/` directory to understand the code structure

## Need Help?

- Check the logs: `docker logs spark-lakehouse`
- Run validation: `./check_setup.sh`
- Review configuration: `cat config/env/dev.yaml`
- Check environment: `env | grep -E "APP_ENV|S3_BUCKET|AWS"`

## Best Practices

1. Always use `.env` file for local development (never commit real credentials)
2. Test with small datasets first
3. Monitor logs for warnings and errors
4. Keep configuration files in sync with your infrastructure
5. Use production configuration for large datasets

## Security Notes

- Never commit `.env` file with real credentials
- Use AWS IAM roles instead of hardcoded credentials when possible
- Restrict S3 bucket access to necessary IAM users
- Rotate AWS credentials regularly
- Review CloudTrail logs for access patterns
