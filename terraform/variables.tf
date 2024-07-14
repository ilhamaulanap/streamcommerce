variable "gcp_project" {
  description = "The ID of your GCP project"
  type        = string
}

variable "gcp_region" {
  description = "The GCP region for resources"
  type        = string
}

variable "credentials" {
    description = "Credential for cloud provisioning"
    default = "./credentials/sa_keys.json"
    type =  string
}

variable "gcs_bucket" {
  description = "The name of the GCS bucket for terraform backend"
  type        = string
}

variable "gcp_zone" {
  description = "The GCP zone for resources"
  type        = string
}

variable "gcs_bucket_location" {
  description = "The location of the GCS bucket for terraform backend"
  type        = string
}
 

variable "kafka_instance_name" {
  description = "The name of the kafka cluster Engine instance"
  type        = string
}

variable "kafka_instance_type" {
  description = "The machine type of the kafka cluster Engine instance"
  type        = string
}

variable "kafka_instance_zone" {
  description = "The zone of the kafka cluster Engine instance"
  type        = string
}

variable "kafka_disk_size" {
  description = "The kafka compute engine disk size"
  type      = number
}

variable "kafka_port" {
  description = "kafka ports"
  type = string
}

variable "kafka_control_port" {
  description = "kafka ports"
  type = string
}

variable "compute_instance_image" {
  description = "The image for the Compute Engine instance"
  type        = string
}

variable "dataproc_instance_name" {
  description = "The name of the dataproc cluster Engine instance"
  type        = string
}

variable "dataproc_instance_master_type" {
  description = "The machine type of the dataproc cluster master node instance"
  type        = string
}

variable "dataproc_master_boot_disk" {
  description = "The disk size of the dataproc cluster master node instance"
  type        = number
}

variable "dataproc_instance_worker_type" {
  description = "The machine type of the dataproc cluster worker node instance"
  type        = string
}

variable "dataproc_worker_boot_disk" {
  description = "The disk size of the dataproc cluster worker node instance"
  type        = number
}

variable "dataproc_instance_image" {
  description = "The image of the dataproc cluster instance"
  type        = string
}

variable "network" {
  description = "Network for your instance/cluster"
  default     = "default"
  type        = string
}

variable "stg_bq_dataset" {
  description = "staging dataset in Big Query"
  type = string
}


variable "prod_bq_dataset" {
  description = "prod dataset in Big Query"
  type = string
}