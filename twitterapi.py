import requests
from requests_oauthlib import OAuth1

# Replace with your keys and tokens
consumer_key = "PLh4yR6IRL06ey0t5eDuCisNy"
consumer_secret = "D0dyjpV5nySsfUgApr0sOey285yVj3gMWbPfCM6Uf1OBcQvQOF"
access_token ="1411971933025959939-7wJ4EY1eNWY0N5Dfc0uliEHSYBjcwV"
access_token_secret = "mODXFPBldy8As7pPDkrbpQxJlkqPCbvkuy37Fxe6Xn3hE"
auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
params = {"screen_name": "yash19014055", "count": 5}

response = requests.get(url, auth=auth, params=params)
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code} - {response.json()}")
