import requests
import json

# --- Config ---
VISA_ID = 319
API_URL = "https://api.visasbot.com/api/visa/list"
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# --- Slack Notification Function ---
def send_slack_alert(visa_info):
    message = {
        "text": f"🎯 *Visa Slot Alert* — `{visa_info['center']}` is now *{visa_info['status'].upper()}*",
        "attachments": [
            {
                "fields": [
                    {"title": "Visa Category", "value": visa_info['visa_category'], "short": True},
                    {"title": "Visa Type", "value": visa_info['visa_type'], "short": True},
                    {"title": "Last Available Date", "value": visa_info.get('last_available_date', 'N/A'), "short": True},
                    {"title": "Last Open At", "value": visa_info.get('last_open_at', 'N/A'), "short": True},
                ]
            }
        ]
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=message)
    if response.status_code != 200:
        print(f"Slack error: {response.text}")
    else:
        print("✅ Slack alert sent.")

# --- Check Visa Status ---
def check_status():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        visas = response.json()["data"]["visas"]

        visa = next((v for v in visas if v["id"] == VISA_ID), None)

        if not visa:
            print(f"Visa ID {VISA_ID} not found.")
            return

        print("=== Visa Slot Info ===")
        print(json.dumps(visa, indent=4))

        if visa["status"].lower() == "open":
            send_slack_alert(visa)

    except Exception as e:
        print(f"Error occurred: {e}")

# --- Run Script ---
if __name__ == "__main__":
    check_status()
