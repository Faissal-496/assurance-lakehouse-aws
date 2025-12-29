# Runtime Contract

## Execution Model

- Apache Spark runs in local mode
- No distributed cluster is assumed
- Jobs are executed either locally (development) or on EC2 (validation)

## Resource Constraints

- EC2 instances are cost-optimized and limited in CPU and memory
- Pipelines must tolerate constrained resources
- Full data rewrites are discouraged

## Failure Model

- Jobs may be interrupted at any point
- Partial writes to S3 are possible
- All pipelines must be idempotent and safe to re-run

## Observability

- Structured logs and metrics are written to S3
- CloudWatch usage is minimal and optional
