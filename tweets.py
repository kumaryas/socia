import tweepy

# Twitter API credentials (Replace with your new credentials)
consumer_key = 'your_new_consumer_key'
consumer_secret = 'your_new_consumer_secret'
access_token = 'your_new_access_token'
access_token_secret = 'your_new_access_token_secret'

# Setup Twitter API authentication
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Try to fetch tweets
try:
    tweets = api.user_timeline(screen_name="twitter_user", count=5)  # Replace 'twitter_user' with the actual username
    for tweet in tweets:
        print(tweet.text)
except tweepy.TweepError as e:
    print(f"Error fetching tweets: {e}")
