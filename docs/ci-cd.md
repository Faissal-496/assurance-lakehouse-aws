# CI/CD

## Flux
- GitHub déclenche Jenkins via webhook
- Pipeline BUILD: lint, tests, validation DAGs
- Pipeline INFRA: build images, push ECR, Terraform plan/apply

## Agents
- BUILD: pas d’accès AWS
- INFRA: rôle IAM avec permissions d’infrastructure

