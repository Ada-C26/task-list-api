import os
import requests

SLACK_URL = "https://slack.com/api/chat.postMessage"


def send_slack_notification(task):
    headers = {
        "Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"
    }

    message = {
        "channel": os.environ.get("SLACK_CHANNEL_ID"),
        "text": f"Someone just completed the task {task.title}"
    }

    requests.post(SLACK_URL, json=message, headers=headers)