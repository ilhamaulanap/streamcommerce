from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryDeleteTableOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'load_data_to_staging_dataset',
    default_args=default_args,
    description='Load data from GCS to staging tables in BigQuery',
    schedule_interval='*/10 * * * *',  # Run every 10 minutes
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# GCS bucket and base file path
GCS_BUCKET_NAME = 'streamcommerce_202407'
GCS_BASE_PATH = 'events_data/'

# BigQuery project and dataset
BQ_PROJECT_ID = 'black-machine-422712-b7'
BQ_STAGING_DATASET_NAME = 'staging_streamcommerce'

# List of tables to delete
tables_to_delete = ['views', 'transactions', 'traffic', 'feedback']

# Function to create BigQueryDeleteTableOperator tasks
def create_delete_table_task(table_name):
    return BigQueryDeleteTableOperator(
        task_id=f'delete_{table_name}_table',
        deletion_dataset_table=f'{BQ_PROJECT_ID}.{BQ_STAGING_DATASET_NAME}.{table_name}',
        ignore_if_missing=True,
        dag=dag,
    )

# Create deletion tasks for each table
delete_table_tasks = [create_delete_table_task(table) for table in tables_to_delete]

# Function to create GCSToBigQueryOperator tasks
def create_gcs_to_bq_task(data_type):
    return GCSToBigQueryOperator(
        task_id=f'load_{data_type}_to_bq',
        bucket=GCS_BUCKET_NAME,
        source_objects=[f'{GCS_BASE_PATH}{data_type}/year=*/month=*/day=*/hour=*/file*.parquet'],
        destination_project_dataset_table=f'{BQ_PROJECT_ID}.{BQ_STAGING_DATASET_NAME}.{data_type}',
        source_format='PARQUET',
        write_disposition='WRITE_TRUNCATE',  # Replace existing data
        create_disposition='CREATE_IF_NEEDED',  # Create table if it does not exist
        dag=dag,
    )

# List of data types
data_types = ['views', 'transactions', 'traffic', 'feedback']

# Create tasks for each data type
gcs_to_bq_tasks = [create_gcs_to_bq_task(data_type) for data_type in data_types]

# Set up task dependencies
for delete_task in delete_table_tasks:
    delete_task >> gcs_to_bq_tasks

# Print DAG structure for verification
print(dag)
