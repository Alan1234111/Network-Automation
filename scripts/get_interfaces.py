#!/usr/bin/env python

import os
import requests
import urllib3
from dotenv import load_dotenv

from webex_alert import send_webex_message

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

ROUTER_IP = os.getenv("ROUTER_IP")
ROUTER_USER = os.getenv("ROUTER_USER")
ROUTER_PASS = os.getenv("ROUTER_PASS")

def get_device_interfaces():

    print(f"I'm connecting with the router {ROUTER_IP}...")

    # RESTCONF ENDPOINT
    url = f"https://{ROUTER_IP}/restconf/data/ietf-interfaces:interfaces"

    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json"
    }

    try:

        response = requests.get(
            url,
            auth=(ROUTER_USER, ROUTER_PASS),
            headers=headers,
            verify=False
        )

        response.raise_for_status()

        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error connection with the device: {e}")
        return None

def display_and_report_interfaces(data):

    if not data:
        print("No data to display.")
        return

    interfaces = data["ietf-interfaces:interfaces"]["interface"]

    print("----- Interfaces found -----")
    print(f"{'Name':<25} | {'Type':<30} | {'State'}")
    print("-" * 75)

    up_count = 0
    down_count = 0

    for interface in interfaces:
        name = interface.get("name", "N/A")
        if_type = interface.get("type", "N/A").split(":")[-1]
        status = "UP" if interface.get("enabled", False) else "DOWN"

        if status == "UP":
            up_count += 1
        else:
            down_count +=1

        print(f"{name:<25} | {if_type:<30} | {status}")

    report = (
        f"Report from the device ({ROUTER_IP})**\n"
        f"> Interfaces retrived via RESTCONF. \n"
        f"> Interfaces up (UP): **{up_count}**\n"
        f"> Interfaces down (DOWN): **{down_count}**\n"
        f"> Status: Operation completed successfully"
    )

    print("Sending a message to the Webex...")
    send_webex_message(report)

    
if __name__ == "__main__":
    interface_data = get_device_interfaces()
    display_and_report_interfaces(interface_data)