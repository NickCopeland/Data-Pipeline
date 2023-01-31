import sys
import datetime
import pandas as pd
import praw
import configparser
import pathlib
import numpy as np
"""
Use Reddit API to retrieve data and export to csv
"""


# Dictionary to store data
fields = []
post_dict = (
    "id",
    "title",
    "score",
    "num_comments",
    "author",
    "created_utc",
    "url",
    "upvote_ratio",
    "over_18",
    "edited",
    "spoiler",
    "stickied",
)

# Read credentials from file
script_path = pathlib.Path(__file__).parent.resolve()
parser = configparser.ConfigParser()
parser.read(f"{script_path}/credentials.ini")
cred_secret = parser.get("reddit_credentials", "secret")
cred_client_id = parser.get("reddit_credentials", "client_id")

def start_log():
    """Start of log file"""
    #logging.info("----------------Start of Log----------------")

def end_log():
    """End of log file"""
    #logging.info("----------------End of Log------------------")

def logp(s):
    """Print and write a string to the log"""
    print(s)
    #logging.info(s)

def log_error_string():
    """Write error to log file along with error details"""
    #logging.info('ERROR: \nError Description: {} \nError at line: {}'.format(sys.exc_info()[1], sys.exc_info()[2].tb_lineno))

def connect_api():
    """Connect to the Reddit API using Python Reddit API Wrapper (PRAW)"""
    # Create PRAW instance
    praw_inst = praw.Reddit(client_id=cred_client_id, client_secret=cred_secret, user_agent="Data_Pipeline_Agent")
    return praw_inst

def main():
    """Extract data from Reddit to CSV"""
    # Process start time
    start_stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    print(start_stamp + ": " + __file__ + " started")


    # Connect to the Reddit API using PRAW
    praw_inst = connect_api()
    
    
    # Set subreddit (forum)
    subreddit = praw_inst.subreddit("dataengineering")


    # Retrieve posts
    posts = subreddit.top(time_filter='day', limit=10)


    # Add posts to dataframe
    for submission in posts:
        to_dict = vars(submission)
        sub_dict = {field: to_dict[field] for field in post_dict}
        fields.append(sub_dict)
        posts_df = pd.DataFrame(fields)

    # transform data
    posts_df["created_utc"] = pd.to_datetime(posts_df["created_utc"], unit="s")
    posts_df["over_18"] = np.where((posts_df["over_18"] == "False") | (posts_df["over_18"] == False), False, True).astype(bool)
    posts_df["edited"] = np.where((posts_df["edited"] == "False") | (posts_df["edited"] == False), False, True).astype(bool)
    posts_df["spoiler"] = np.where((posts_df["spoiler"] == "False") | (posts_df["spoiler"] == False), False, True).astype(bool)
    posts_df["stickied"] = np.where((posts_df["stickied"] == "False") | (posts_df["stickied"] == False), False, True).astype(bool)


    # Use this for local machine testing
    output = __file__.replace(".py", ".csv")
    posts_df.to_csv(output, index=False)

    # Use this for Airflow
    #posts_df.to_csv(f"/tmp/{output_name}.csv", index=False)

if __name__ == "__main__":
    try:
        main()
    
    # Error handling
    except Exception as e:
        # Print error and line number
        logp('ERROR: {} \r\nLINE: {}'.format(sys.exc_info()[1], sys.exc_info()[2].tb_lineno))