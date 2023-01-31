import sys
import configparser
import pathlib
import psycopg2
"""
Upload CSV from S3 to Redshift
"""

# Read credentials from file
script_path = pathlib.Path(__file__).parent.resolve()
parser = configparser.ConfigParser()
parser.read(f"{script_path}/credentials.ini")
account_id = parser.get("aws_config", "account_id")
bucket = parser.get("aws_config", "bucket")
username = parser.get("aws_config", "redshift_username")
password = parser.get("aws_config", "redshift_password")
host = parser.get("aws_config", "redshift_hostname")
port = parser.get("aws_config", "redshift_port")
redshift_role = parser.get("aws_config", "redshift_role")
database = parser.get("aws_config", "redshift_database")


# Variables
table_name = "Data_Engineering"
staging_table = table_name + "_Stage"
csv_to_load = "extract_to_csv.csv"
file_path = "s3://" + bucket + "/" + csv_to_load
role_string = "arn:aws:iam::" + account_id + ":role/" + redshift_role


# Store SQL Queries in strings
create_table_final = "CREATE TABLE IF NOT EXISTS " + table_name + """ (
            id varchar PRIMARY KEY,
            title varchar(max),
            num_comments int,
            score int,
            author varchar(max),
            created_utc timestamp,
            url varchar(max),
            upvote_ratio float,
            over_18 bool,
            edited bool,
            spoiler bool,
            stickied bool
        );"""
create_table_staging = "CREATE TEMP TABLE " + staging_table + " (LIKE " + table_name + ");"
load_table_staging = "COPY " + staging_table + " FROM '" + file_path + "' iam_role '" + role_string + "' IGNOREHEADER 1 DELIMITER ',' CSV;"
remove_duplicates = "DELETE FROM " + table_name + " USING " + staging_table + " WHERE " + table_name + ".id = " + staging_table + ".id;"
load_table_final = "INSERT INTO " + table_name + " SELECT * FROM " + staging_table + ";"
drop_staging_table = "DROP TABLE " + staging_table + ";"


def main():
    """Populate Redshift table from CSV file in S3 bucket"""
    conn = psycopg2.connect(dbname=database, 
                                    host=host,
                                    port=port,
                                    user=username, 
                                    password=password)
    # Create cursor
    cur = conn.cursor()

    # Run queries
    cur.execute(create_table_final)
    cur.execute(create_table_staging)
    cur.execute(load_table_staging)
    cur.execute(remove_duplicates)
    cur.execute(load_table_final)
    cur.execute(drop_staging_table)

    # Commit changes
    conn.commit()

    # Close cursor and connection
    cur.close()
    conn.close()

    print("Process complete")


if __name__ == "__main__":
    main()