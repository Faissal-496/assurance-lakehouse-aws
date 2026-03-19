# Deployment

## Pré-requis
- AWS account et accès IAM
- S3 bucket pour state Terraform
- DynamoDB pour lock Terraform
- Certificat ACM pour ALB

## Terraform
Exécuter Terraform depuis les environnements:

- terraform/envs/dev
- terraform/envs/staging
- terraform/envs/prod

Exemple:
terraform init
terraform plan
terraform apply

## Airflow
Les instances Airflow démarrent via user_data et docker compose.
Les DAGs sont synchronisés via GitSync.

