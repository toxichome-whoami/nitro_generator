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
    """Basic validation for Discord webhook URLs."""
    return webhook_url.startswith("https://discord.com/api/webhooks/") and len(webhook_url) > 50

def generate_random_character():
    """Generate a random string (5-18 characters)."""
    characters = string.ascii_letters
    length = random.randint(5, 18)
    return ''.join(random.choice(characters) for _ in range(length))

def send_message(webhook_url, message):
    try:
        response = requests.post(webhook_url, json={"content": message}, headers={'Content-Type': 'application/json'})
        response.raise_for_status()  
        return True
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return False


def main():
    try:
        print(f"{COLORS['HEADER']}**Discord Gift Link Generator Made by Toxic Home**{COLORS['ENDC']}")
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

        # Generate and send Discord gift links
        while True:
            try:
                message_generat = int(input(f"{COLORS['BLUE']}How many Discord gift links do you want to generate and send?{COLORS['ENDC']}: "))
                if message_generat <= 0:
                    raise ValueError
                break
            except ValueError:
                print(f"{COLORS['RED']}Invalid input. Please enter a positive integer.{COLORS['ENDC']}")

        success_count = 0
        failure_count = 0

        for _ in tqdm(range(message_generat), desc="Progress", unit="Messages"):
            random_character = generate_random_character()
            message = f"https://discord.gift/{random_character}"
            message_sent = send_message(webhook_url, message)
            if message_sent:
                success_count += 1
                print(f"{COLORS['GREEN']}Message '{random_character}' sent successfully!{COLORS['ENDC']}", end='\r')
            else:
                failure_count += 1
                print(f"{COLORS['RED']}Failed to send message.{COLORS['ENDC']}", end='\r')
            time.sleep(0.8)


        print(f"\n{COLORS['BOLD']}**Message Sending Statistics**{COLORS['ENDC']}")
        print("-----------------------------------------")
        print(f"{COLORS['GREEN']}**Success:** {success_count}/{message_generat} messages sent successfully!{COLORS['ENDC']}")
        print(f"{COLORS['RED']}**Failure:** {failure_count}/{message_generat} messages failed to send.{COLORS['ENDC']}")
        print("-----------------------------------------")
        print(f"{COLORS['BLUE']}**Webhook URL:** {webhook_url}{COLORS['ENDC']}")
        print("-----------------------------------------")
        print(f"{COLORS['HEADER']}**Discord Gift Link Generator Made by Toxic Home**{COLORS['ENDC']}")
        print(f"{COLORS['YELLOW']}Exiting...{COLORS['ENDC']}\n")
        time.sleep(1)  # brief pause before exit
    except Exception as e:
        print(f"{COLORS['RED']}An unexpected error occurred: {e}{COLORS['ENDC']}")
        print("Exiting due to error.")
        time.sleep(1)  # Brief pause before exit

if __name__ == '__main__':
    main()
