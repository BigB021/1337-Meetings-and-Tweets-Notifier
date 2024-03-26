## 1337 School Twitter and Website Notifier

This project contains two Python scripts designed to notify the user of new tweets from 1337 School's Twitter account and changes to the meetings page on the 1337 website.

# Features 

Twitter Notification: Monitors the 1337 School's Twitter account for new tweets and plays a notification sound when a new tweet is detected.
Website Change Notification: Monitors the 1337 School's meetings webpage for any changes (e.g., new meeting announcements) and plays a notification sound when changes are detected.

# Requirements 

1. Python 3.x
2. feedparser for parsing the RSS feed for Twitter notifications.
3. playwright for automating website interaction and monitoring changes.
4. beautifulsoup4 for parsing HTML content of the webpage.
5. An external tool like mpg123 for playing notification sounds.

## Installation 

1. Clone this repository to your local machine.
2. Navigate to the project directory and install the required Python packages:

    pip install feedparser playwright beautifulsoup4

3. Install the playwright browser instances:

    playwright install

4. (Optional) If using a custom sound player, ensure it is installed and available in your system's PATH. For example, to install mpg123 on Ubuntu:

    sudo apt-get install mpg123

## Configuration

Before running the scripts, you need to configure a few environment variables for the website notifier script:

**MY_EMAIL:**  Your login email for the 1337 website.
**MY_PASSWORD:** Your password for the 1337 website.
It's recommended to set these variables in your shell's profile file (e.g., .bashrc, .profile) to keep them secure:

    export MY_EMAIL='your_email@example.com'
    export MY_PASSWORD='your_password'

## Usage

1. Twitter Notification Script
To start monitoring for new tweets from the 1337 School's Twitter account, run:

    python twitter_notifier_script.py

2. Website Change Notification Script
To start monitoring for changes on the 1337 School's meetings webpage, run:

    python website_notifier_script.py

## Important Notes

Ensure the RSS feed URL in the Twitter notification script is up-to-date.
Modify the notification sound file paths in the scripts if you're using custom notification sounds.
The scripts will continue to run and check for updates periodically. To stop them, simply interrupt the execution (e.g., by pressing Ctrl+C in the terminal).

**Author: Youssef AITBOUDDROUB**

This README provides a basic overview and instructions for setting up and running the scripts. You can adjust the content as needed, especially if you decide to integrate more features or change the configuration process.
