import tweepy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BEARER_TOKEN = os.getenv("BEARER_TOKEN")


client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Replace 'user_id' with an actual user ID
user_id = '44196397'  # Example user ID (Elon Musk)

try:
    tweets = client.get_users_tweets(id=user_id, max_results=1)
    for tweet in tweets.data:
        print(tweet.text)
except Exception as e:
    print(f"Error: {e}")
