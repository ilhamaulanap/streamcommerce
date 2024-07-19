from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from schemas.schemas import transactions_schema, traffic_schema, feedback_schema, views_schema  
from task_functions import create_external_table, create_empty_table, insert_bq


# GCS bucket and base file path
GCS_BUCKET_NAME = 'streamcommerce_202407_update'
GCS_BASE_PATH = 'events_data'

# BigQuery project and dataset
BQ_PROJECT_ID = 'black-machine-422712-b7'
BQ_STAGING_DATASET_NAME = 'staging_streamcommerce'

# List of EVENTS to process
EVENTS = ['views', 'transactions', 'traffic', 'feedback']

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
with DAG(
    'load_to_bigquery',
    default_args=default_args,
    description='Load to bigquery from gcs',
    schedule_interval='*/10 * * * *',  # Run every 10 minute
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    initiate_dbt_task = BashOperator(
        task_id='dbt_initiate',
        bash_command='cd /dbt && dbt deps --profiles-dir . --target prod'
    )


    execute_dbt_task = BashOperator(
        task_id = 'dbt_run',
        bash_command = 'cd /dbt && dbt deps && dbt run --profiles-dir . --target prod'
    )


    for EVENT in EVENTS:
        
        BQ_STAGING_TABLE_NAME = EVENT
        INSERT_QUERY = f"{{% include 'sql/{EVENT}.sql' %}}" 
        BQ_DATASET_EXTERNAL_TABLE = f'{BQ_PROJECT_ID}.{BQ_STAGING_DATASET_NAME}.{EVENT}_external'
        SCHEMA = globals()[f'{EVENT}_schema']
        

        create_external_table_task = create_external_table(EVENT,
                                                            GCS_BUCKET_NAME, 
                                                            GCS_BASE_PATH, 
                                                            BQ_DATASET_EXTERNAL_TABLE,  
                                                            SCHEMA)
        
        create_empty_table_task = create_empty_table(EVENT,
                                                        BQ_STAGING_DATASET_NAME,
                                                        BQ_STAGING_TABLE_NAME,
                                                        BQ_PROJECT_ID,
                                                        SCHEMA)
                                                
        execute_insert_query_task = insert_bq(EVENT,
                                                INSERT_QUERY)
    


        create_external_table_task >> \
        create_empty_table_task >> \
        execute_insert_query_task >> \
        initiate_dbt_task >> \
        execute_dbt_task

