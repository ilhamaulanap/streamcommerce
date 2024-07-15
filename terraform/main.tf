provider "google" {
  credentials = var.credentials #use credentials if run locally
  project     = var.gcp_project
  region      = var.gcp_region
}

resource "google_storage_bucket" "bucket" {
  name          = var.gcs_bucket
  location      = var.gcs_bucket_location
  force_destroy = true

  uniform_bucket_level_access = true

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 # days
    }
  }
}


resource "google_compute_instance" "kafka_instance" {
  name         = var.kafka_instance_name
  machine_type = var.kafka_instance_type
  zone         = var.kafka_instance_zone

  boot_disk {
    initialize_params {
      size = var.kafka_disk_size
      image = var.compute_instance_image
    }
  }

  network_interface {
    network = "default"
    access_config {
      // This will create an external IP address for the instance
    }
  }
}

resource "google_dataproc_cluster" "mulitnode_spark_cluster" {
  name   = var.dataproc_instance_name
  region = var.gcp_region

  cluster_config { 

    staging_bucket = var.gcs_bucket

    gce_cluster_config {
      internal_ip_only = false
      network = var.network
      zone    = var.gcp_zone

      shielded_instance_config {
        enable_secure_boot = true
      }
    }

    master_config {
      num_instances = 1
      machine_type  = var.dataproc_instance_master_type
      disk_config {
        boot_disk_type    = "pd-ssd"
        boot_disk_size_gb = var.dataproc_master_boot_disk
      }
    }

    worker_config {
      num_instances = 2
      machine_type  = var.dataproc_instance_worker_type
      disk_config {
        boot_disk_size_gb = var.dataproc_worker_boot_disk
      }
    }

    software_config {
      image_version = var.dataproc_instance_image
      override_properties = {
        "dataproc:dataproc.allow.zero.workers" = "true"
      }
      optional_components = ["JUPYTER"]
    }

  }

}



resource "google_compute_firewall" "port_rules" {
  project     = var.gcp_project
  name        = "kafka-broker"
  network     = var.network
  description = "Opens port 9092 in the Kafka VM"

  allow {
    protocol = "tcp"
    ports    = [var.kafka_port]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "kafka_port_rules" {
  project     = var.gcp_project
  name        = "kafka-control"
  network     = var.network
  description = "Opens port 9092 in the Kafka VM"

  allow {
    protocol = "tcp"
    ports    = [var.kafka_control_port]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "allow_http" {
  project     = var.gcp_project
  name        = "allow-http"
  network     = var.network
  description = "Opens port 80 in the Kafka VM"

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "allow_https" {
  project     = var.gcp_project
  name        = "allow-https"
  network     = var.network
  description = "Opens port 80 in the Kafka VM"

  allow {
    protocol = "tcp"
    ports    = ["443"]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_bigquery_dataset" "stg_dataset" {
  dataset_id                 = var.stg_bq_dataset
  project                    = var.gcp_project
  delete_contents_on_destroy = true
}

resource "google_bigquery_dataset" "prod_dataset" {
  dataset_id                 = var.prod_bq_dataset
  project                    = var.gcp_project
  delete_contents_on_destroy = true
}



