import sys
import configparser
import pathlib
import psycopg2
import csv
import sys
import boto3
import botocore

"""
Download data from Redshift to CSV which will be used to load dashboard
"""
# Read credentials from file
script_path = pathlib.Path(__file__).parent.resolve()
parser = configparser.ConfigParser()
parser.read(f"{script_path}/credentials.ini")


# Store configuration variables
account_id = parser.get("aws_config", "account_id")
s3_bucket = parser.get("aws_config", "bucket")
username = parser.get("aws_config", "redshift_username")
password = parser.get("aws_config", "redshift_password")
host = parser.get("aws_config", "redshift_hostname")
port = parser.get("aws_config", "redshift_port")
redshift_role = parser.get("aws_config", "redshift_role")
database = parser.get("aws_config", "redshift_database")
table_name = "data_engineering_transformed"
unload_destination = 's3://' + s3_bucket + '/export/redshift_export_'
output = __file__.replace(".py", ".csv")


def main():
    """Connect to Redshift, unload data to S3 bucket as CSV then download the CSV"""
    # Connect to Redshift
    conn = psycopg2.connect(dbname=database, 
                                    host=host,
                                    port=port,
                                    user=username, 
                                    password=password)
    cur = conn.cursor()
    
    # Unload to S3 as CSV
    sql_string = "UNLOAD ('SELECT * FROM " + table_name + """')
        TO '""" + unload_destination + """'
        iam_role 'arn:aws:iam::""" + account_id + ":role/" + redshift_role + """'
        region 'us-west-1'
        CSV
        ALLOWOVERWRITE
        parallel off"""
    cur.execute(sql_string)
    conn.commit()
    conn.close()

    # Connect to AWS S3
    s3 = boto3.resource("s3")

    # Download CSV
    s3.meta.client.download_file(s3_bucket,'export/redshift_export_000',output)
    
    

if __name__ == "__main__":
    main()