# Architecture

## Vue globale
La plateforme suit un modèle Lakehouse sur AWS avec Airflow en haute disponibilité, Spark pour le traitement, et Terraform pour l’infrastructure.

## Flux principal
- GitHub héberge le code, les DAGs et Terraform
- Jenkins déclenche la CI/CD et construit les images
- Les images sont poussées dans ECR
- Airflow récupère les DAGs via GitSync
- Les jobs Spark s’exécutent via EMR Serverless

## Composants
- ALB public HTTPS pour Jenkins et Airflow
- EC2 privés pour Jenkins et Airflow
- Amazon MQ pour Celery
- RDS PostgreSQL pour Airflow
- S3 pour le Data Lake
- Glue pour le catalogue

