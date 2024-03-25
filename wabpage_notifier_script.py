# Author : Youssef AITBOUDDROUB
# Notify user when changes occurs in the meetings page in 1337 website

import os
import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import subprocess  # For playing sound without heavy dependencies

# Using environment variables to store credentials
email = os.getenv("MY_EMAIL")
password = os.getenv("MY_PASSWORD")
site = "https://candidature.1337.ma/meetings"
notification_sound_path = "notification.mp3"

def play_notification_sound():
    subprocess.call(["mpg123", "-q", notification_sound_path])

def sign_in(page, email, password):
    page.goto(site, wait_until='networkidle')
    print("Filling email input..\n")
    # Update the selector to match the email input field
    page.fill('input[name="user[email]"]', email)  # Use '#user_email' for ID selector
    print("Filling password input..\n")
    # Update the selector to match the password input field
    page.fill('input[name="user[password]"]', password)  # Use '#user_password' for ID selector
    print("Submitting...\n")
    page.click('input[type="submit"][value="Sign in"]')
    page.wait_for_load_state('networkidle')


def get_page_content(page):
    html_content = page.content()
    soup = BeautifulSoup(html_content, 'html.parser')
    for element in soup(["script", "style", "iframe", "meta"]):
        element.decompose()
    clean_text = soup.get_text()
    return clean_text.strip()

def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)  # Set headless=False to see the browser
        page = browser.new_page()
        sign_in(page, email, password)
        current_content = get_page_content(page)
        browser.close()

        try:
            with open("last_content.txt", 'r') as file:
                last_content = file.read()
        except FileNotFoundError:
            last_content = None
        os.system('cls' if os.name == 'nt' else 'clear') # Clear terminal
        if current_content != last_content:
            print("Changes detected!!")
            t_end = time.time() + 60 * 5 # Play the notification for 5 minutes
            while time.time() < t_end:
                play_notification_sound()
            with open("last_content.txt", 'w') as file:
                file.write(current_content)
        else:
            print("No changes detected.")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(300)  # Check every 5 minutes

