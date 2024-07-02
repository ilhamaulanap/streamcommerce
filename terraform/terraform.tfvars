
#Backend for terraform 
#backend_bucket          = "kafka-terraform-state-backend-202402"

gcs_bucket     = "streamcommerce_202407"
gcs_bucket_location     = "ASIA"

gcp_project               = "black-machine-422712-b7"
gcp_region                = "asia-southeast1 "

compute_instance_image    = "ubuntu-os-cloud/ubuntu-2004-lts"

kafka_instance_name     = "streamcommerce"
kafka_instance_type     = "e2-standard-2"
kafka_instance_zone     = "asia-southeast1-b"
kafka_port              = "9092"
kafka_control_port      = "9021"
kafka_disk_size         = 50


stg_bq_dataset = "staging_streamcommerce"
prod_bq_dataset = "prod_streamcommerce"



# change this to path of your gcp key files if you want to run this repo locally
credentials               = "credentials/sa_keys.json" # create a secret in github and add the gcp key 