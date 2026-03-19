# ============================================================================
# GLUE MODULE - INPUT VARIABLES
# ============================================================================

variable "database_name" {
  type        = string
  description = "Name of Glue Catalog database"
  default     = "lakehouse"
}

variable "description" {
  type        = string
  description = "Database description"
  default     = "Lakehouse metadata catalog"
}

variable "tags" {
  type        = map(string)
  description = "Tags to apply"
  default     = {}
}
