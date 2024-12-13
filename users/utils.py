import requests
import tweepy
from django.conf import settings

# def test_twitter_connection():
#     try:
#         auth = tweepy.OAuth1UserHandler(
#             settings.TWITTER_API_KEY,
#             settings.TWITTER_API_SECRET,
#             'user_access_token',  # Replace with actual user token
#             'user_access_token_secret'  # Replace with actual user token secret
#         )
#         api = tweepy.API(auth)
#         user = api.verify_credentials()
#         if user:
#             print(f"Authenticated as: {user.screen_name}")
#         else:
#             print("Failed to authenticate.")
#     except Exception as e:
#         print(f"Error connecting to Twitter API: {e}")

def get_user_tweets(user):
    try:
        consumer_key = settings.TWITTER_API_KEY
        consumer_secret = settings.TWITTER_API_SECRET
        access_token = user.profile.twitter_access_token
        access_token_secret = user.profile.twitter_access_token_secret

        # Tweepy authentication
        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        api = tweepy.API(auth)

        # Verify credentials
        user_details = api.verify_credentials()
        if user_details:
            print(f"Twitter user authenticated: {user_details.screen_name}")
        else:
            print("Twitter authentication failed.")

        # Fetch tweets
        return api.user_timeline(screen_name=user.profile.twitter_handle, count=5)
    except tweepy.Unauthorized as e:
        print(f"Twitter authentication error: {e}")
        raise
    except Exception as e:
        print(f"General error fetching tweets: {e}")
        raise


def get_instagram_posts(user):
    try:
        access_token = user.profile.instagram_access_token  # Ensure 'profile' model has 'instagram_access_token'
        url = f'https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,timestamp&access_token={access_token}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('data', [])
    except Exception as e:
        print(f"Error fetching Instagram posts: {e}")
        return []
