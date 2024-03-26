# Author : Youssef AITBOUDDROUB
# Notify user when new tweets are posted on the 1337 coding school X page

import os
import feedparser
import time
from webpage_notifier_script import play_notification_sound
import threading
from datetime import datetime,timedelta

# RSS feed URL for 1337 Twitter account
RSS_FEED_URL = "https://rss.app/feeds/JGpDkNgtajBxdNBJ.xml"
NOTIFICATION_SOUND_PATH = "notification2.mp3"

# Calculates script's execution duration and displays it
def display_execution_time(start_time):
    # Initial sleep to prevent immediate printing and allow other messages to display first
    time.sleep(0.1)
    while not stop_thread.is_set():
        elapsed_time = timedelta(seconds=int(time.time() - start_time))
        print(f'\rExecution Time: {elapsed_time}', end='')
        time.sleep(1)

def check_for_new_tweets(feed_url):
    feed = feedparser.parse(feed_url)
    return feed.entries

def main():
    # Initially, get all current tweets to establish a baseline
    current_entries = check_for_new_tweets(RSS_FEED_URL)
    last_entry_id = current_entries[0].id if current_entries else None

    while True:
        entries = check_for_new_tweets(RSS_FEED_URL)
        if entries and entries[0].id != last_entry_id:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
            print("⚠︎ ⚠︎ New tweet detected! ⚠︎ ⚠︎")
            t_end = time.time() + 20  # Play the notification for 20 seconds
            while time.time() < t_end:
                play_notification_sound()
            last_entry_id = entries[0].id
        
        print("\n\nSleeping for 5 minutes before checking again...(っ- ‸ - ς)ᶻ 𝗓 𐰁")  
        time.sleep(300)

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear') 
    start_time = time.time()
    stop_thread = threading.Event()
    # Get current time to monitor when script started
    now = datetime.now()
    startTime = now.strftime("%H:%M:%S")
    print("Execution started at: ",startTime)
    print("Monitoring new tweets...")

    # Start the execution time display thread after the initial message
    clock_thread = threading.Thread(target=display_execution_time, args=(start_time,))
    clock_thread.start()
    try:
        main()
    finally:
        stop_thread.set()
        clock_thread.join()
        print("\nScript execution completed.")
