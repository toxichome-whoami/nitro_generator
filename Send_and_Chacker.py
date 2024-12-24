import requests
import json
import random
import string
import time
import os
from tqdm import tqdm  # for animated loading indicator

# Constants
WEBHOOK_FILE = 'webhook_link_save.txt'
COLORS = {
    'HEADER': '\033[95m',
    'BLUE': '\033[94m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'RED': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m'
}

def load_webhook_from_file():
    """Load webhook URL from file, if it exists."""
    if os.path.exists(WEBHOOK_FILE):
        with open(WEBHOOK_FILE, 'r') as file:
            return file.read().strip()
    return None

def save_webhook_to_file(webhook_url):
    """Save webhook URL to file."""
    with open(WEBHOOK_FILE, 'w') as file:
        file.write(webhook_url)

def get_webhook_from_user():
    """Prompt user for webhook URL and save it to file."""
    while True:
        webhook_url = input(f"{COLORS['BLUE']}Enter your Discord webhook URL{COLORS['ENDC']}: ")
        if validate_webhook_url(webhook_url):
            save_webhook_to_file(webhook_url)
            return webhook_url
        else:
            print(f"{COLORS['RED']}Invalid webhook URL. Please try again.{COLORS['ENDC']}")

def validate_webhook_url(webhook_url):
    """Validate the Discord webhook URL by sending a test request."""
    if not webhook_url.startswith("https://discord.com/api/webhooks/"):
        return False
    try:
        response = requests.head(webhook_url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def generate_random_character():
    """Generate a random string (5-18 characters)."""
    characters = string.ascii_letters + string.digits
    length = random.randint(16, 24)  # Adjusted for typical Nitro code length
    return ''.join(random.choice(characters) for _ in range(length))

def check_nitro_gift_link(link):
    """Check if a Discord Nitro gift link is valid."""
    try:
        response = requests.head(link)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def send_message(webhook_url, message):
    try:
        response = requests.post(
            webhook_url,
            json={"content": message},
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 429:
            retry_after = response.json().get("retry_after", 1)
            print(f"Rate limited. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)
            return send_message(webhook_url, message)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return False


def main():
    try:
        print(f"{COLORS['HEADER']}**Discord Gift Link Generator & Checker Made by Toxic Home**{COLORS['ENDC']}")
        print("-----------------------------------------")

        # Load webhook URL from file, or prompt user if it doesn't exist
        webhook_url = load_webhook_from_file()
        if not webhook_url:
            print(f"{COLORS['YELLOW']}No webhook URL found. Please enter a valid URL.{COLORS['ENDC']}")
            webhook_url = get_webhook_from_user()

        # Ask user if they want to update the webhook URL
        update_webhook = input(f"{COLORS['BLUE']}Using webhook URL: {webhook_url}\nDo you want to update it? (y/n){COLORS['ENDC']}: ")
        if update_webhook.lower() == 'y':
            webhook_url = get_webhook_from_user()

        # Generate, check, and send Discord Nitro gift links
        while True:
            try:
                message_generat = int(input(f"{COLORS['BLUE']}How many Discord Nitro gift links do you want to generate and check?{COLORS['ENDC']}: "))
                if message_generat <= 0:
                    raise ValueError
                break
            except ValueError:
                print(f"{COLORS['RED']}Invalid input. Please enter a positive integer.{COLORS['ENDC']}")

        success_count = 0
        failure_count = 0
        sent_count = 0

        for _ in tqdm(range(message_generat), desc="Progress", unit="Links"):
            random_character = generate_random_character()
            link = f"https://discord.gift/{random_character}"

            # Check if the generated link is valid (not redeemed and exists)
            if check_nitro_gift_link(link):
                success_count += 1
                print(f"{COLORS['GREEN']}Valid link found: {link}{COLORS['ENDC']}")

                # Send the valid link via webhook
                if send_message(webhook_url, link):
                    sent_count += 1
                    print(f"{COLORS['GREEN']}Link sent successfully via webhook!{COLORS['ENDC']}")
                else:
                    print(f"{COLORS['RED']}Failed to send link via webhook.{COLORS['ENDC']}")
            else:
                failure_count += 1
                print(f"{COLORS['RED']}Invalid link: {link}{COLORS['ENDC']}", end='\r')
            time.sleep(0.1)  # Brief delay to avoid overwhelming the Discord API


        print(f"\n{COLORS['BOLD']}**Link Generation & Sending Statistics**{COLORS['ENDC']}")
        print("-----------------------------------------")
        print(f"{COLORS['GREEN']}**Valid Links Found:** {success_count}/{message_generat}{COLORS['ENDC']}")
        print(f"{COLORS['RED']}**Invalid Links:** {failure_count}/{message_generat}{COLORS['ENDC']}")
        print(f"{COLORS['GREEN']}**Links Sent via Webhook:** {sent_count}/{success_count} (of valid links){COLORS['ENDC']}")
        print("-----------------------------------------")
        print(f"{COLORS['BLUE']}**Webhook URL:** {webhook_url}{COLORS['ENDC']}")
        print("-----------------------------------------")
        print(f"{COLORS['HEADER']}**Discord Gift Link Generator & Checker Made by Toxic Home**{COLORS['ENDC']}")
        print(f"{COLORS['YELLOW']}Exiting...{COLORS['ENDC']}\n")
        time.sleep(1)  # Brief pause before exit
    except Exception as e:
        print(f"{COLORS['RED']}An unexpected error occurred: {e}{COLORS['ENDC']}")
        print("Exiting due to error.")
        time.sleep(1)  # Brief pause before exit

if __name__ == '__main__':
    main()
    