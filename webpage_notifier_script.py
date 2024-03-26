import os
import time
import subprocess
import threading
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
email = os.getenv("MY_EMAIL")
password = os.getenv("MY_PASSWORD")
site = "https://candidature.1337.ma/meetings"
notification_sound_path = "notification.mp3"

class WebMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.execution_start_display = f"Execution started at: {datetime.now().strftime('%H:%M:%S')}"
        self.stop_thread = threading.Event()
        self.lock = threading.Lock()

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
        subprocess.call(["mpg123", "-q", notification_sound_path])

    def sign_in(self, page, email, password):
        page.goto(site, wait_until='networkidle')
        print("\nFilling email input...")
        page.fill('input[name="user[email]"]', email)
        print("Filling password input...")
        page.fill('input[name="user[password]"]', password)
        print("Submitting...")
        page.click('input[type="submit"][value="Sign in"]')
        page.wait_for_load_state('networkidle')

    def get_page_content(self, page):
        html_content = page.content()
        soup = BeautifulSoup(html_content, 'html.parser')
        for element in soup(["script", "style", "iframe", "meta"]):
            element.decompose()
        return soup.get_text().strip()

    def main(self):
        while True:
            with sync_playwright() as p:
                browser = p.firefox.launch(headless=True)
                page = browser.new_page()
                self.sign_in(page, email, password)
                current_content = self.get_page_content(page)
                browser.close()

                try:
                    with open("last_content.txt", 'r') as file:
                        last_content = file.read()
                except FileNotFoundError:
                    last_content = None
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
                if current_content != last_content:
                    self.log_message("⚠︎ ⚠︎ Changes detected!! ⚠︎ ⚠︎")
                    t_end = time.time() + 60 * 5  # Notification duration
                    while time.time() < t_end:
                        self.play_notification_sound()
                    with open("last_content.txt", 'w') as file:
                        file.write(current_content)
                else:
                    self.log_message("No changes detected.")
                
                print("\n\nSleeping for 5 minutes before checking again...(っ- ‸ - ς)ᶻ 𝗓 𐰁")  
                time.sleep(300)

if __name__ == "__main__":
    monitor = WebMonitor()
    threading.Thread(target=monitor.display_execution_time, daemon=True).start()
    monitor.main()
