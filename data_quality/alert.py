"""Send data quality alerts to Slack."""

import os
from slack_sdk import WebClient
from data_quality.expectations import run_quality_checks


def send_slack_alert(results, passed):
    token = os.environ.get("SLACK_BOT_TOKEN")
    channel = os.environ.get("SLACK_CHANNEL", "#data-alerts")
    if not token:
        print("No SLACK_BOT_TOKEN set, skipping alert")
        return

    client = WebClient(token=token)

    blocks = [
        {"type": "header", "text": {"type": "plain_text",
            "text": "Data Quality: ALL PASSED" if passed else "Data Quality: FAILURES DETECTED"}},
        {"type": "divider"},
    ]

    for r in results:
        emoji = ":white_check_mark:" if r["passed"] else ":x:"
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"{emoji} *{r['check']}*: `{r['value']}`"}
        })

    client.chat_postMessage(channel=channel, blocks=blocks, text="Data Quality Report")
    print(f"Alert sent to {channel}")


if __name__ == "__main__":
    results, passed = run_quality_checks()
    send_slack_alert(results, passed)
