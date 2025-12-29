# AWS Assumptions

This document lists all AWS resources assumed to exist before running
the Lakehouse project.

## AWS Account

- Environment: Development
- Cloud Provider: AWS
- Region: eu-west-1

## Existing Resources

### Amazon S3

- Bucket: `lakehouse-assurance-dev`
- Versioning: enabled
- Server-side encryption: enabled
- Bucket acts as:
  - primary data lake storage
  - state store for logs and job metadata

### AWS Glue

- Glue Catalog enabled
- Glue Database: `lakehouse_assurance_dev`
- Used exclusively for metadata management

### Compute

- EC2 instance available for execution
- Docker installed and running
- Outbound access to S3 and Glue

### IAM

- IAM managed outside this repository
- EC2 instance uses an attached IAM role
- No static AWS credentials are allowed

## Out of Scope

- Lifecycle rules
- Cost allocation and tagging
- Network configuration
