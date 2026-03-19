# AWS Glue Crawlers for Automatic Schema Discovery
# Enables metadata management and Glue Catalog integration

resource "aws_glue_crawler" "bronze_crawler" {
  name          = "${local.name_prefix}-bronze-crawler"
  database_name = aws_glue_catalog_database.lakehouse.name
  role          = aws_iam_role.glue_crawler_role.arn
  
  s3_target {
    path = "s3://${aws_s3_bucket.data_lake.id}/bronze/"
  }
  
  schedule = "cron(0 5 * * ? *)"  # Daily at 5 AM, after ingestion
  
  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "UPDATE_IN_DATABASE"
  }
  
  configuration = jsonencode({
    Version = 1.0
    CrawlerOutput = {
      Partitions = { AddOrUpdateBehavior = "InheritFromTable" }
      Tables     = { AddOrUpdateBehavior = "MergeNewColumns" }
    }
  })
  
  tags = local.common_tags
}

resource "aws_glue_crawler" "silver_crawler" {
  name          = "${local.name_prefix}-silver-crawler"
  database_name = aws_glue_catalog_database.lakehouse.name
  role          = aws_iam_role.glue_crawler_role.arn
  
  s3_target {
    path = "s3://${aws_s3_bucket.data_lake.id}/silver/"
  }
  
  schedule = "cron(0 6 * * ? *)"  # Daily at 6 AM
  
  tags = local.common_tags
}

# IAM Role for Glue Crawlers
resource "aws_iam_role" "glue_crawler_role" {
  name = "${local.name_prefix}-glue-crawler-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
  
  tags = local.common_tags
}

# S3 access policy for Glue Crawlers
resource "aws_iam_role_policy" "glue_crawler_s3" {
  name = "${local.name_prefix}-glue-crawler-s3"
  role = aws_iam_role.glue_crawler_role.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.data_lake.arn,
          "${aws_s3_bucket.data_lake.arn}/*"
        ]
      }
    ]
  })
}

# Glue Catalog database access
resource "aws_iam_role_policy_attachment" "glue_crawler_catalog_policy" {
  role       = aws_iam_role.glue_crawler_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

# CloudWatch Logs policy for Glue
resource "aws_iam_role_policy" "glue_crawler_logs" {
  name = "${local.name_prefix}-glue-crawler-logs"
  role = aws_iam_role.glue_crawler_role.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:/aws-glue/*"
      }
    ]
  })
}

# Glue Crawler trigger (optional - for dependent crawlers)
resource "aws_glue_trigger" "crawler_trigger" {
  name            = "${local.name_prefix}-crawler-sequential-trigger"
  type            = "CONDITIONAL"
  enabled         = true
  workflow_name   = aws_glue_workflow.etl_workflow.name
  
  actions {
    job_name = aws_glue_crawler.silver_crawler.name
  }
  
  predicate {
    logical   = "ANY"
    conditions {
      crawler_name         = aws_glue_crawler.bronze_crawler.name
      crawl_state          = "SUCCEEDED"
    }
  }
}

# Glue Workflow for orchestration (optional)
resource "aws_glue_workflow" "etl_workflow" {
  name = "${local.name_prefix}-etl-workflow"
  
  tags = local.common_tags
}

# Outputs for Glue resources
output "glue_database_name" {
  description = "Glue Catalog database name"
  value       = aws_glue_catalog_database.lakehouse.name
}

output "bronze_crawler_name" {
  description = "Bronze layer Glue Crawler name"
  value       = aws_glue_crawler.bronze_crawler.name
}

output "silver_crawler_name" {
  description = "Silver layer Glue Crawler name"
  value       = aws_glue_crawler.silver_crawler.name
}
