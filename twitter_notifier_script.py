# Author : Youssef AITBOUDDROUB
# Notify the user when new tweets are posted on the X page of the 1337 coding school

import os
import feedparser
import time
from wabpage_notifier_script import play_notification_sound

# RSS feed URL for 1337 Twitter account
RSS_FEED_URL = "https://rss.app/feeds/JGpDkNgtajBxdNBJ.xml"
NOTIFICATION_SOUND_PATH = "notification2.mp3"

def check_for_new_tweets(feed_url):
    feed = feedparser.parse(feed_url)
    return feed.entries

def main():
    print("Monitoring new tweets...")
    last_checked = time.time()
    
    # Initially, get all current tweets to establish a baseline
    current_entries = check_for_new_tweets(RSS_FEED_URL)
    last_entry_id = current_entries[0].id if current_entries else None
    
    while True:
        entries = check_for_new_tweets(RSS_FEED_URL)
        if entries and entries[0].id != last_entry_id:
            os.system('cls' if os.name == 'nt' else 'clear') # Clear terminal
            print("New tweet detected!")
            t_end = time.time() + 20 # Play the notification for 20 seconds
            while time.time() < t_end:
                play_notification_sound()
            last_entry_id = entries[0].id
        
        # Wait for a specified time before checking again (e.g., 5 minutes)
        time.sleep(300)

if __name__ == "__main__":
    main()
