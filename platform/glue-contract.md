# Glue Catalog Contract

## Purpose

AWS Glue Catalog is used as a centralized metadata repository.

## Rules

- Glue Crawlers are explicitly forbidden
- Tables are created and updated programmatically via Spark
- One Glue database per environment

## Schema Management

- Schemas are defined in code
- Backward compatibility is preferred
- Breaking schema changes require explicit approval
