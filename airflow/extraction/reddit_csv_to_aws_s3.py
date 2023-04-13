import sys
import datetime
import configparser
import pathlib
import boto3
import botocore
import logging
"""
Upload CSV data to S3 bucket
"""

# Read credentials from file
script_path = pathlib.Path(__file__).parent.resolve()
parser = configparser.ConfigParser()
parser.read(f"{script_path}/credentials.ini")
s3_bucket = parser.get("aws_config", "bucket")
region = parser.get("aws_config", "region")
logger = logging.getLogger("airflow.task")

# File info
csv_to_load = "extract_to_csv.csv"

def main():
    """Upload input file to S3 bucket"""
    # Process start time
    start_stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    print(start_stamp + ": " + __file__ + " started")
    logger.error("My script path: " + str(script_path))
    
    # Connect to AWS S3
    s3 = boto3.resource("s3")

    # Create the bucket if it doesn't already exist
    create_bucket_if_needed(s3)

    # Upload the file
    s3.meta.client.upload_file(Filename=str(script_path) + "/" + csv_to_load, Bucket=s3_bucket, Key=csv_to_load)



def create_bucket_if_needed(s3):
    """Create the bucket if needed"""
    try:
        s3.meta.client.head_bucket(Bucket=s3_bucket)
    except botocore.exceptions.ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "404":
            logger.error("bucket doesn't exist")


if __name__ == "__main__":
    main()