# Deployment & Ops Checklist (Lakehouse Platform)

## 1) Repository Structure
- [ ] `docker/airflow/Dockerfile` exists
- [ ] `docker/spark/Dockerfile` exists
- [ ] `docker/compose/docker-compose.yml` exists
- [ ] `docker/compose/docker-compose-aws.yml` exists
- [ ] `orchestration/airflow/dags/` contains DAGs (GitSync expects repo path)

## 2) Required Environment Variables
### Local (docker/compose/docker-compose.yml)
- [ ] `.env` present at repo root
- [ ] `GIT_SYNC_REPO` set
- [ ] `GIT_SYNC_BRANCH` set
- [ ] `DB_USER/DB_PASSWORD/DB_NAME` set

### AWS (docker/compose/docker-compose-aws.yml)
- [ ] `.env.aws` present
- [ ] `AIRFLOW_IMAGE` set
- [ ] `AIRFLOW_DB_CONN` set
- [ ] `AIRFLOW_RESULT_BACKEND` set
- [ ] `AIRFLOW_BROKER_URL` set (`amqps://...`)
- [ ] `AIRFLOW_FERNET_KEY` set
- [ ] `AIRFLOW_WEBSERVER_SECRET_KEY` set
- [ ] `GIT_SYNC_REPO` set
- [ ] `GIT_SYNC_BRANCH` set

## 3) Terraform (envs)
- [ ] `terraform/envs/dev/terraform.tfvars` created
- [ ] `terraform/envs/staging/terraform.tfvars` created
- [ ] `terraform/envs/prod/terraform.tfvars` created
- [ ] `alb_certificate_arn` valid in each env
- [ ] `airflow_image_tag` set to Jenkins short SHA
- [ ] `enable_secrets_manager` set as needed

## 4) Versions (Pinned)
- Airflow: `2.7.3`
- Python (Airflow base): `3.10`
- Spark: `3.5.0`
- Hadoop AWS: `3.3.4`
- AWS SDK bundle: `1.12.262`
- PostgreSQL: `15.x`
- Terraform: `>= 1.0`
- AWS Provider: `~> 5.0`
- GitSync: `v4.1.0`

## 5) Security
- [ ] RDS SSL enforced (`rds_force_ssl = true`)
- [ ] ALB HTTPS enabled
- [ ] Airflow logs to S3 enabled
- [ ] Secrets Manager enabled for prod (recommended)

## 6) CI/CD
- [ ] Jenkins builds images with `short SHA`
- [ ] Jenkins runs Terraform from `terraform/envs/${ENVIRONMENT}`
- [ ] Build agent has no AWS access
- [ ] Infra agent uses Jenkins IAM role

