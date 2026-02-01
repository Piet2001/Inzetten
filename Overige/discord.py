import requests
import os
import time

def webhook(title, message, color="16711680"):

    webhook_url = os.getenv("DISCORD")
    embed = {
        "title": title,
        "description": message,
        "color": color,
    }
    webhookdata = {
        "username": "MKS GameTeam Bot",
        "embeds": [
            embed
        ],
    }

    headers = {
        "Content-Type": "application/json"
    }

    result = requests.post(webhook_url, json=webhookdata, headers=headers)
    if 200 <= result.status_code < 300:
        print(f"Webhook sent {result.status_code}")
        time.sleep(3)
    else:
        print(f"Not sent with {result.status_code}, response:\n{result.json()}")