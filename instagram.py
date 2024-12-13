import requests

# Instagram API access token and user ID
access_token = 'your_valid_instagram_access_token'
user_id = 'user_id_of_the_profile'  # Make sure the user profile is public

# Fetch Instagram profile data
url = f'https://graph.instagram.com/{user_id}?fields=id,username&access_token={access_token}'

response = requests.get(url)
data = response.json()

if 'error' in data:
    print("Error fetching Instagram posts:", data['error'])
else:
    print("Instagram profile data:", data)
