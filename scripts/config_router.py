#!/usr/bin/env python

import os
import json
import yaml
import requests
import urllib3
import ipaddress
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
from webex_alert import send_webex_message

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
ROUTER_IP = os.getenv("ROUTER_IP")
ROUTER_USER = os.getenv("ROUTER_USER")
ROUTER_PASS = os.getenv("ROUTER_PASS")

script_dir = Path(__file__).parent

def main():
    print("1. Loading data from vars.yml...")
    vars_path = script_dir / "vars.yml"
    with open(vars_path, "r") as f:
        vars_dict = yaml.safe_load(f)

    # Check if IP Address is correct
    ip_str = vars_dict["ip_address"]
    try:
        ipaddress.IPv4Address(ip_str)
    except ipaddress.AddressValueError:
        print(f"ERROR: vars.yml contains incorrect IP address: {ip_str}")
        exit(1)

    print("2. Printing JSON payload from Jinja2 template...")
    env = Environment(loader=FileSystemLoader(script_dir))
    template = env.get_template("template.j2")

    rendered_json_str = template.render(vars_dict)
    payload = json.loads(rendered_json_str)

    interface_name = vars_dict["interface_name"]

    print(f"3. Sending config to the router (PATCH {interface_name})...")
    url = f"https://{ROUTER_IP}/restconf/data/ietf-interfaces:interfaces/interface={interface_name}"
    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json"
    }

    try:
        # Sending PUT
        response = requests.put(url, auth=(ROUTER_USER, ROUTER_PASS), headers=headers, json=payload, verify=False)
        response.raise_for_status()

        print("4. Configuration send! Verification of the changes...")
        verify_response = requests.get(url, auth=(ROUTER_USER, ROUTER_PASS), headers={"Accept": "application/yang-data+json"}, verify=False)

        configured_data = verify_response.json()
        configured_ip = configured_data["ietf-interfaces:interface"][0]["ietf-ip:ipv4"]["address"][0]["ip"]

        print(f" --- SUCCESS! Interface {interface_name} have now IP: {configured_ip}")

        print("5. Sendind message to Webex...")
        send_webex_message(f"Interface updated {interface_name}, New IP address: {configured_ip}")

    except requests.exceptions.HTTPError as err:
        print(f"Error HTTP: {err}")
        print(f"Details: {response.text}")

if __name__ == "__main__":
    main()