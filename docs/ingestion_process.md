# Ingestion Process

## Source Files

- Source files (e.g. Excel) are treated as immutable
- Files are read once and converted to Parquet

## Frequency

- Monthly ingestion batches
- Deterministic batch identifiers are used

## Guarantees

- No duplicate ingestion
- Safe re-processing
- Full traceability through logs
