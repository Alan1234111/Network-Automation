#!/usr/bin/env python

import os
import requests
from dotenv import load_dotenv

load_dotenv()

WEBEX_TOKEN = os.getenv("WEBEX_TOKEN")
WEBEX_ROOM_ID = os.getenv("WEBEX_ROOM_ID")

def send_webex_message(message_text):

    if not WEBEX_TOKEN or not WEBEX_ROOM_ID:
        print("ERROR: Missing WEBEX_TOKEN or WEBEX_ROOM_ID. Check .env file!")
        return False


    url = " https://webexapis.com/v1/messages"

    headers = {
        "Authorization": f"Bearer {WEBEX_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "roomId": WEBEX_ROOM_ID,
        "markdown": message_text
    }

    try:
        print(f"Sending Webex Notification to company room...")

        response = requests.post(url, headers=headers, json=payload)

        response.raise_for_status()

        print("Success! Message has been sent. ")
        return True

    except requests.exceptions.RequestException as e:
        
        print(f"Error: We could not send the message. Details: {e}")
        return False

if __name__ == "__main__":
    test_message = "**Phase 1 ** Scirpts was successful 🎉"
    send_webex_message(test_message)