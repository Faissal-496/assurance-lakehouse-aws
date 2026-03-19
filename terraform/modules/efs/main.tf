# ============================================================================
# TERRAFORM MODULE: EFS (Shared Storage)
# ============================================================================

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_efs_file_system" "this" {
  creation_token = var.name_prefix
  encrypted      = var.encrypted

  performance_mode = var.performance_mode
  throughput_mode  = var.throughput_mode

  tags = merge(
    var.tags,
    {
      Name = "${var.name_prefix}-efs"
    }
  )
}

resource "aws_efs_mount_target" "this" {
  for_each = toset(var.subnet_ids)

  file_system_id  = aws_efs_file_system.this.id
  subnet_id       = each.value
  security_groups = var.security_group_ids
}
