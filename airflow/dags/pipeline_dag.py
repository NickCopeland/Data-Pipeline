from airflow import DAG
#from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os
import logging
"""
DAG purpose:
    1. Extract Reddit data to CSV
    2. Load CSV into an AWS S3 bucket
    3. Load data from S3 bucket to AWS Redshift
"""

# Output name of extracted file. This be passed to each
# DAG task so they know which file to process
output_name = datetime.now().strftime("%Y%m%d")


with DAG("reddit_pipeline",
    start_date=datetime(2023,1,1),
    max_active_runs=1,
    schedule="@daily",
    description="Reddit pipeline",
    default_args={
        "owner": "airflow", 
        "email_on_failure" : "False",
        "retries" : 0,
        "retry_delay" : timedelta(minutes=1)
    },
    catchup=False,
    tags=["RedditETL"],
    #template_searchpath='/opt/airflow/extraction/' # path to the python files
) as dag:
    csv_extract = BashOperator(
        task_id="csv_extract",
        bash_command=f"python /opt/airflow/extraction/extract_to_csv.py {output_name}",
        dag=dag,
    )
    csv_extract.doc_md = "Extract Reddit data and store as CSV"

    csv_to_s3 = BashOperator(
        task_id="csv_to_s3",
        bash_command=f"python /opt/airflow/extraction/reddit_csv_to_aws_s3.py {output_name}",
        dag=dag,
    )
    csv_to_s3.doc_md = "Upload Reddit CSV data to S3 bucket"

    s3_to_redshift = BashOperator(
        task_id="s3_to_redshift",
        bash_command=f"python /opt/airflow/extraction/s3_to_redshift.py {output_name}",
        dag=dag,
    )
    s3_to_redshift.doc_md = "Copy S3 CSV file to Redshift table"

# Define task dependencies
csv_extract >> csv_to_s3 >> s3_to_redshift