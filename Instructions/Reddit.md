
# Create a Reddit account 
[link](https://www.reddit.com/register/)

# Request an application
[link](https://www.reddit.com/prefs/apps/)

Once created take note of
1. client_id (displayed in the top left under "personal use script")
2. secret key

Return to the [link](https://www.reddit.com/prefs/apps/) at any time to retrieve these values again

# Set up credentials
Update the credentials file `~/Data-Pipeline/Python/credentials.ini`

	```credentials
	[reddit_credentials]
	secret = XXXX
	client_id = XXXX
	```

