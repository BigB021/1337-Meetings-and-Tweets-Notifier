import os
import time
import tweepy
from dotenv import load_dotenv
import subprocess

# Load environment variables
load_dotenv()

# Twitter API credentials
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Notification sound path
notification_sound_path = "notification2.mp3"

def play_notification_sound():
    subprocess.call(["mpg123", "-q", notification_sound_path])
    print("Notification played!")

def get_client():
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    return client

def check_for_new_tweet(client, user_id, last_tweet_id=None):
    try:
        tweets = client.get_users_tweets(id=user_id, max_results=1)
        if tweets.data:
            latest_tweet_id = tweets.data[0].id
            if last_tweet_id is None or latest_tweet_id != last_tweet_id:
                return True, latest_tweet_id
        return False, last_tweet_id
    except tweepy.TweepyException as e:
        print(f"Error fetching tweets: {e}")
        return False, last_tweet_id


def main():
    client = get_client()
    user_id = "971012509032427520"  # User ID for @1337FIL
    last_tweet_id = None
    
    while True:
        has_new_tweet, last_tweet_id = check_for_new_tweet(client, user_id, last_tweet_id)
        if has_new_tweet:
            print("New tweet detected!")
            play_notification_sound()
        else:
            print("No new tweets.")
        time.sleep(300)  # Check every 5 minutes

if __name__ == "__main__":
    main()
