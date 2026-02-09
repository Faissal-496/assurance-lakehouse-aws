# Lakehouse Architecture

## Overview

This project implements a lightweight Lakehouse architecture on AWS designed
for cost efficiency, resilience, and analytical use cases.

## Core Components

- Amazon S3 as the primary storage layer
- Apache Spark for batch data processing
- AWS Glue Catalog for metadata management
- EC2 for execution with strict cost control

## Key Design Principles

- Stateless and idempotent pipelines
- Explicit data contracts
- Minimal AWS services usage
- Cost-aware engineering
