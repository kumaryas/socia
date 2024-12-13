# social_media_dashboard/views.py
from django.conf import settings
from django.http import HttpResponse


import tweepy
from django.shortcuts import render
from decouple import config


def test_keys(request):
    twitter_key = settings.TWITTER_API_KEY
    twitter_secret = settings.TWITTER_API_SECRET
    return HttpResponse(f"TWITTER_API_KEY: {twitter_key}<br>TWITTER_API_SECRET: {twitter_secret}")


# Fetch Twitter API keys from .env file
consumer_key = config('TWITTER_API_KEY')
consumer_secret = config('TWITTER_API_SECRET')
access_token = config('TWITTER_ACCESS_TOKEN', default='dummy-token')  # Optional, if available
access_token_secret = config('TWITTER_ACCESS_TOKEN_SECRET', default='dummy-secret')  # Optional, if available

# Authentication using tweepy and Twitter API credentials
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# View to fetch tweets
def fetch_tweets(request):
    try:
        # Fetch the latest tweets from your timeline
        tweets = api.home_timeline(count=5)
        # Display the tweets in a template
        return render(request, 'social_media_dashboard/tweets.html', {'tweets': tweets})
    except tweepy.TweepError as e:
        return render(request, 'social_media_dashboard/error.html', {'error': str(e)})
