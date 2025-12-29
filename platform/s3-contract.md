# S3 Storage Contract

## Bucket Layout

The S3 bucket follows a layered Lakehouse structure:

- bronze/   : raw ingested data
- silver/   : cleaned and standardized datasets
- gold/     : business-oriented datasets
- logs/     : execution logs and metrics
- archive/  : cold or deprecated data

## Rules

- Each dataset owns a dedicated prefix
- No job may write outside its assigned prefix
- Partitioning must be deterministic and documented

## Data Mutability

- Bronze data is append-only
- Silver and Gold data may be overwritten at partition level
- Overwrites must be idempotent
