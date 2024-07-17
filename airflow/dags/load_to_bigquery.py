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

# List of tables to delete and load
tables_to_process = ['views', 'transactions', 'traffic', 'feedback']

# Function to create delete and load tasks for each table
def create_delete_and_load_tasks(table_name):
    # Delete table task
    delete_task = BigQueryDeleteTableOperator(
        task_id=f'delete_{table_name}_table',
        deletion_dataset_table=f'{BQ_PROJECT_ID}.{BQ_STAGING_DATASET_NAME}.{table_name}',
        ignore_if_missing=True,
        dag=dag,
    )
    
    # Load from GCS to BigQuery task
    load_task = GCSToBigQueryOperator(
        task_id=f'load_{table_name}_to_bq',
        bucket=GCS_BUCKET_NAME,
        source_objects=[f'{GCS_BASE_PATH}{table_name}/year=*/month=*/day=*/hour=*/file*.parquet'],
        destination_project_dataset_table=f'{BQ_PROJECT_ID}.{BQ_STAGING_DATASET_NAME}.{table_name}',
        source_format='PARQUET',
        write_disposition='WRITE_TRUNCATE',  # Replace existing data
        create_disposition='CREATE_IF_NEEDED',  # Create table if it does not exist
        dag=dag,
    )
    
    # Set task dependencies
    delete_task >> load_task
    
    return delete_task, load_task

# Create tasks for each table
delete_and_load_tasks = [create_delete_and_load_tasks(table) for table in tables_to_process]

# Print DAG structure for verification
print(dag)
