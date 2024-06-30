# Author : Youssef AITBOUDDROUB
# Notify user when pool is available

import os
import time
import subprocess
import threading
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pygame

# Load environment variables
load_dotenv()
email = os.getenv("MY_EMAIL")
password = os.getenv("MY_PASSWORD")
print(email, password)
sign_in_page = "https://admission.1337.ma/en/users/sign_in"
pool_page = "https://admission.1337.ma/candidature/piscine"
notification_sound_path = "notification2.mp3"
content_file = "pool_page_content.txt"

class PoolMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.execution_start_display = f"Execution started at: {datetime.now().strftime('%H:%M:%S')}"
        self.stop_thread = threading.Event()
        self.lock = threading.Lock()
        self.is_signed_in = False  # Track sign-in status

    def display_execution_time(self):
        while not self.stop_thread.is_set():
            with self.lock:
                elapsed_time = timedelta(seconds=int(time.time() - self.start_time))
                print(f'\r{self.execution_start_display} | Execution Time: {elapsed_time}', end='')
            time.sleep(1)

    def log_message(self, message):
        with self.lock:
            # Move up one line and clear line
            print("\033[F\033[K")
            print(message)
            # Ensure the execution time display is reprinted after logging
            elapsed_time = timedelta(seconds=int(time.time() - self.start_time))
            print(f'{self.execution_start_display} | Execution Time: {elapsed_time}', end='')


    def play_notification_sound(self):
        # Initialize pygame mixer
        pygame.mixer.init()

        # Load the sound file
        sound = pygame.mixer.Sound(notification_sound_path)

        # Play the sound
        sound.play()

        # Wait for the sound to finish playing
        while pygame.mixer.get_busy():
            pygame.time.delay(100)

    def sign_in(self, page, email, password):
        if not self.is_signed_in:
            page.goto(sign_in_page, wait_until='domcontentloaded', timeout=60000)
            print("\nFilling email input...")
            page.fill('input[type="email"]', email)
            print("Filling password input...")
            page.fill('input[type="password"]', password)
            print("Submitting...")
            page.click('button:text("SIGN IN")')
            page.wait_for_load_state('networkidle')
            self.is_signed_in = True  # Update sign-in status

    def get_page_content(self, page):
        html_content = page.content()
        soup = BeautifulSoup(html_content, 'html.parser')
        for element in soup(["script", "style", "iframe", "meta"]):
            element.decompose()
        return soup.get_text().strip()
    
    def check_pool_availability(self, page):
        pool_container_selector = 'div.flex.flex-col.justify-center.items-center.bg-gray-100.p-20.rounded-sm'
        available_text = "Any available Pool will appear here"
        if page.text_content(pool_container_selector).strip() == available_text:
            print("No available pools at the moment.")
        else:
            print("There are available pools!")

    def main(self):
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=True)
            page = browser.new_page()
            self.sign_in(page, email, password)  # Sign in once
            page.goto(pool_page, wait_until='domcontentloaded', timeout=60000)  # Go directly to pool page
            while True:
                current_content = self.get_page_content(page)
                self.check_pool_availability(page)

                try:
                    with open(content_file, 'r') as file:
                        last_content = file.read()
                except FileNotFoundError:
                    last_content = None

                os.system('cls' if os.name == 'nt' else 'clear')
                if current_content != last_content:
                    self.log_message("⚠︎ ⚠︎ Changes detected!! ⚠︎ ⚠︎")
                    self.notify_changes()
                    print("current content:", current_content)
                    with open(content_file, 'w') as file:
                        file.write(current_content)
                else:
                    self.log_message("No changes detected.")

                print("\n\nSleeping for 5 minutes before checking again...(っ- ‸ - ς)ᶻ 𝗓 𐰁")
                time.sleep(300)  # Adjusted sleep to 5 minutes

    def notify_changes(self):
        t_end = time.time() + 60 * 5
        while time.time() < t_end:
            self.play_notification_sound()


if __name__ == "__main__":
    monitor = PoolMonitor()
    threading.Thread(target=monitor.display_execution_time, daemon=True).start()
    monitor.main()