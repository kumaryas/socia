from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
import tweepy

# Twitter API credentials
CONSUMER_KEY = 'your_twitter_consumer_key'
CONSUMER_SECRET = 'your_twitter_consumer_secret'
ACCESS_TOKEN = 'your_twitter_access_token'
ACCESS_TOKEN_SECRET = 'your_twitter_access_token_secret'

# Function to authenticate Twitter
def authenticate_twitter():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api

# Function to fetch user tweets
def get_user_tweets(user):
    try:
        api = authenticate_twitter()
        tweets = api.user_timeline(screen_name=user.username, count=5)  # Fetch 5 recent tweets
        return [tweet.text for tweet in tweets]
    except Exception as e:
        print(f"Error fetching tweets: {e}")
        return []

# Function to fetch Instagram posts
def get_instagram_posts(user):
    try:
        access_token = user.profile.instagram_access_token  # Access token from user profile
        if not access_token:
            return []

        url = f'https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,timestamp&access_token={access_token}'
        response = requests.get(url)
        data = response.json()

        if 'data' in data:
            return data['data']  # Return Instagram post data
        else:
            return []
    except Exception as e:
        print(f"Error fetching Instagram posts: {e}")
        return []

# View for the dashboard
@login_required
def dashboard(request):
    # Fetch user data from Twitter and Instagram
    tweets = get_user_tweets(request.user)
    instagram_posts = get_instagram_posts(request.user)

    # Render dashboard template
    return render(request, 'users/dashboard.html', {
        'tweets': tweets,
        'instagram_posts': instagram_posts,
    })

# View for login redirect
def login_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # If logged in, go to dashboard
    return render(request, 'users/login.html')

# View for register redirect
def register_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # If logged in after registration, go to dashboard
    return render(request, 'users/register.html')
