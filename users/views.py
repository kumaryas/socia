import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
import tweepy
from django.core.cache import cache

def some_view(request):
    try:
        auth = tweepy.OAuth1UserHandler(
            settings.TWITTER_API_KEY,
            settings.TWITTER_API_SECRET,
            'user_access_token',  # Replace with actual user token
            'user_access_token_secret'  # Replace with actual user token secret
        )
        api = tweepy.API(auth)
        user = api.verify_credentials()
        if user:
            print(f"Authenticated as: {user.screen_name}")
        else:
            print("Failed to authenticate.")
    except Exception as e:
        print(f"Error connecting to Twitter API: {e}")

    return render(request, 'users/some_template.html')  # Correct path

# Landing page view
def landing_page(request):
    return render(request, 'users/landing_page.html')

# Register view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user
            return redirect('dashboard')  # Redirect to dashboard
        else:
            print(form.errors)  # Print form errors in the console
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print(f"User {user.username} logged in successfully")  # Debug log
            return redirect('users:dashboard_home')
        else:
            print("Invalid form submission")  # Debug log
    else:
        form = AuthenticationForm()
    print("GET request received for login")  # Debug log
    return render(request, 'users/login.html', {'form': form})

# Profile view
@login_required
def profile(request):
    return render(request, 'users/profile.html')

# Function to fetch Instagram posts
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

# Function to fetch Twitter posts
def get_user_tweets(user):
    try:
        # Fetch Twitter API credentials from settings
        consumer_key = settings.TWITTER_API_KEY
        consumer_secret = settings.TWITTER_API_SECRET
        access_token = user.profile.twitter_access_token
        access_token_secret = user.profile.twitter_access_token_secret

        # Authenticate with Twitter API using Tweepy
        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        api = tweepy.API(auth)

        # Fetch the last 5 tweets from the user's timeline
        tweets = api.user_timeline(screen_name=user.profile.twitter_handle, count=5)
        return [tweet.text for tweet in tweets]
    except tweepy.TweepError as e:
        print(f"Error fetching tweets: {e}")
        return []

# Dashboard view (for logged-in user's posts)
@login_required
def dashboard(request):
    user = request.user
    twitter_data = None
    instagram_data = None

    # Fetch Twitter posts
    try:
        twitter_data = get_user_tweets(user)
    except Exception as e:
        twitter_data = f"Error fetching tweets: {e}"

    # Fetch Instagram posts
    try:
        instagram_data = get_instagram_posts(user)
    except Exception as e:
        instagram_data = f"Error fetching Instagram posts: {e}"

    return render(request, 'users/dashboard.html', {
        'twitter_data': twitter_data,
        'instagram_data': instagram_data,
        'user': user,  # Pass the user to the template to display their info
    })


# @login_required
# def dashboard(request):
#     user = request.user
#     twitter_data = None
#     instagram_data = None

#     # Cache keys for user data
#     twitter_cache_key = f"twitter_data_{user.id}"
#     instagram_cache_key = f"instagram_data_{user.id}"

#     # Fetch data from cache
#     twitter_data = cache.get(twitter_cache_key)
#     instagram_data = cache.get(instagram_cache_key)

#     if not twitter_data:
#         try:
#             twitter_data = get_user_tweets(user)
#             if not twitter_data:
#                 twitter_data = ["No tweets available."]
#             cache.set(twitter_cache_key, twitter_data, timeout=3600)  # Cache for 1 hour
#         except tweepy.TweepError as e:
#             twitter_data = [f"Twitter API error: {e}"]
#         except Exception as e:
#             twitter_data = [f"Unknown error fetching tweets: {e}"]

#     if not instagram_data:
#         try:
#             instagram_data = get_instagram_posts(user)
#             if not instagram_data:
#                 instagram_data = ["No Instagram posts available."]
#             cache.set(instagram_cache_key, instagram_data, timeout=3600)  # Cache for 1 hour
#         except requests.exceptions.RequestException as e:
#             instagram_data = [f"Instagram API error: {e}"]
#         except Exception as e:
#             instagram_data = [f"Unknown error fetching Instagram posts: {e}"]

#     return render(request, 'users/dashboard.html', {
#         'twitter_data': twitter_data,
#         'instagram_data': instagram_data,
#         'user': user,
#     })