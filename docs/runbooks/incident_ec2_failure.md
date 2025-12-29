# Runbook: EC2 Failure During Job Execution

## Objective

Provide a clear procedure to diagnose and recover from EC2 failures
without data corruption.

## Procedure

1. Identify the last run log in S3
2. Inspect run status and error details
3. Verify target partitions in S3
4. Decide whether to re-run or fix the issue
5. Re-run safely using the same run_id

## Guarantee

All jobs are designed to be idempotent and safe to re-run.
