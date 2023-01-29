import sys
import datetime
import configparser
import pathlib
import boto3
import botocore
"""
Upload CSV data to S3 bucket
"""

# Read credentials from file
script_path = pathlib.Path(__file__).parent.resolve()
parser = configparser.ConfigParser()
parser.read(f"{script_path}/credentials.ini")
s3_bucket = parser.get("aws_config", "bucket")
region = parser.get("aws_config", "region")

# File info
csv_to_load = "extract_to_csv.csv"

def main():
    """Upload input file to S3 bucket"""
    # Process start time
    start_stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    print(start_stamp + ": " + __file__ + " started")

    # Connect to AWS S3
    conn = boto3.resource("s3")

    # Create the bucket if it doesn't already exist
    create_bucket_if_needed(conn)

    # Upload the file
    conn.meta.client.upload_file(Filename=str(script_path) + "\\" + csv_to_load, Bucket=s3_bucket, Key=csv_to_load)



def create_bucket_if_needed(conn):
    """Create the bucket if needed"""
    exists = True
    try:
        conn.meta.client.head_bucket(Bucket=s3_bucket)
    except botocore.exceptions.ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "404":
            exists = False
    if not exists:
        conn.create_bucket(
            Bucket=s3_bucket,
            CreateBucketConfiguration={"LocationConstraint": region},
        )



if __name__ == "__main__":
    main()