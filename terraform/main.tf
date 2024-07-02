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



