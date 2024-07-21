# Terraform Infra Setup

## Prerequisites

1. Ensure you have [Terraform](https://www.terraform.io/downloads.html) installed.
2. Set up your [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) and authenticate with your GCP account.

## Steps to Setup the Infrastructure

1. **Clone the repository in your local machine.**

    ```bash
    git clone https://github.com/ilhamaulanap/streamcommerce.git && \
    cd streamcommerce/terraform
    ```

2. **Initiate Terraform and download the required dependencies.**

    ```bash
    terraform init
    ```

3. **View the Terraform plan.**

    You will be asked to enter two values, the name of the GCS bucket you want to create and your GCP Project ID. Use the same values throughout the project.

    ```bash
    terraform plan
    ```

4. **Terraform plan should show the creation of following services:**

    - `e2-standard-4` Compute Instance for Kafka
    - `e2-standard-4` Compute Instance for Airflow
    - Dataproc Spark Cluster
        - One `e2-standard-2` Master node
    - A Google Cloud Storage bucket
    - Two BigQuery Datasets
        - staging_streamcommerce
        - prod_streamcommerce
    - Firewall rule to open port `9092` on the Kafka Instance

5. **Apply the infra.**

    **Note:** Billing will start as soon as the apply is complete.

    ```bash
    terraform apply
    ```

6. **Once you are done with the project, teardown the infra using:**

    ```bash
    terraform destroy
    ```

## Terraform Variables

Adjust the following variables in your `terraform.tfvars` file as needed:

```hcl
gcs_bucket = "streamcommerce_202407_update"
gcs_bucket_location = "US"

gcp_project = "black-machine-422712-b7"
gcp_region = "asia-southeast1"
gcp_zone = "asia-southeast1-b"

compute_instance_image = "ubuntu-os-cloud/ubuntu-2004-lts"

kafka_instance_name = "streamcommerce"
kafka_instance_type = "e2-standard-2"
kafka_instance_zone = "asia-southeast1-b"
kafka_port = "9092"
kafka_control_port = "9021"
kafka_disk_size = 50

airflow_instance_name = "streamcommerce-airflow-dbt"
airflow_instance_type = "e2-standard-2"
airflow_instance_zone = "asia-southeast1-b"
airflow_webserver_port = "8080"
airflow_disk_size = 50

dataproc_instance_name = "streamcommerce-spark-cluster"
dataproc_instance_master_type = "e2-highmem-2"
dataproc_master_boot_disk = 50
dataproc_instance_image = "2.1-debian11"

stg_bq_dataset = "staging_streamcommerce"
prod_bq_dataset = "prod_streamcommerce"
