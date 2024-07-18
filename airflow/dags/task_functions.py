from airflow.providers.google.cloud.operators.bigquery import (BigQueryCreateExternalTableOperator, 
                                                               BigQueryCreateEmptyTableOperator, 
                                                               BigQueryExecuteQueryOperator,
                                                            )


def create_external_table(EVENT,
                          GCS_BUCKET_NAME, 
                          GCS_BASE_PATH, 
                          BQ_DATASET_EXTERNAL_TABLE,  
                          SCHEMA):

    task = BigQueryCreateExternalTableOperator(
        task_id=f'create_external_{EVENT}_table',
        bucket=GCS_BUCKET_NAME,
        source_objects=f'{GCS_BASE_PATH}/{EVENT}/*.parquet',  # Adjust source path here
        destination_project_dataset_table=BQ_DATASET_EXTERNAL_TABLE,
        source_format='PARQUET',
        schema_fields=SCHEMA
    )

    return task


def create_empty_table(EVENT,
                       BQ_STAGING_DATASET_NAME,
                       BQ_STAGING_TABLE_NAME,
                       BQ_PROJECT_ID,
                       SCHEMA):
   
    task = BigQueryCreateEmptyTableOperator(
        task_id=f'create_native_{EVENT}_table',
        dataset_id=BQ_STAGING_DATASET_NAME,
        table_id=BQ_STAGING_TABLE_NAME,
        project_id=BQ_PROJECT_ID,
        schema_fields=SCHEMA,
        if_exists='ignore'
    )

    return task

    
def insert_bq(EVENT,
               INSERT_QUERY):
    
    task = BigQueryExecuteQueryOperator(
        task_id=f'insert_into_native_{EVENT}_table',
        sql=INSERT_QUERY,
        use_legacy_sql=False
    )

    return task

