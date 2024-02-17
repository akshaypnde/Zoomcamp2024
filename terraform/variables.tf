variable "bq_dataset_name" {
  description = "My Bigquery Dataset Name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "terraform-demo-397122-terra-bucket"
}

variable "location" {
  description = "Location"
  default     = "EU"
}

variable "project" {
  description = "GC Project Name"
  default     = "proud-climber-399113"
}