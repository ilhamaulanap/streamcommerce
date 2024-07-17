from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator

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
    'load_external_table_bigquery',
    default_args=default_args,
    description='Update external tables in BigQuery hourly as new data arrives in GCS',
    schedule_interval='@hourly',  # Run every hour
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# GCS bucket and base file path
GCS_BUCKET_NAME = 'streamcommerce_202407_update'
GCS_BASE_PATH = 'events_data'

# BigQuery project and dataset
BQ_PROJECT_ID = 'black-machine-422712-b7'
BQ_STAGING_DATASET_NAME = 'staging_streamcommerce'

# List of tables to process
tables_to_process = ['views', 'transactions', 'traffic', 'feedback']

# Function to create tasks for defining or updating external tables
def create_external_table_tasks(table_name):
    # Create or update external table task
    external_table_task = BigQueryCreateExternalTableOperator(
        task_id=f'update_external_{table_name}_table_hourly',
        bucket=GCS_BUCKET_NAME,
        source_objects=[f'{GCS_BASE_PATH}/{table_name}/*.parquet'],  # Adjust source path here
        destination_project_dataset_table=f'{BQ_PROJECT_ID}.{BQ_STAGING_DATASET_NAME}.{table_name}',
        source_format='PARQUET',
        dag=dag,
    )
    
    return external_table_task

# Create tasks for each table to define or update external tables
external_table_tasks = [create_external_table_tasks(table) for table in tables_to_process]

# Set dependencies for external table tasks
for external_table_task in external_table_tasks:
    external_table_task

# Print DAG structure for verification
print(dag)
