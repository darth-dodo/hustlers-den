import os
import sys
import logging
import json
import requests

from integrations.constants import SLACK_WEBHOOK_CHANNEL_URL

logger = logging.getLogger(__name__)

def post_message_to_slack_channel(message):
    """
    """

    if not message:
        logger.warning("Empty message being passed to Slack app")

    payload = {
                "text": message
            }

    json_payload = json.dumps(payload)

    response = requests.post(url=SLACK_WEBHOOK_CHANNEL_URL, data=json_payload)

    if not response.ok:
        logger.error("Posting message on Slack failed with status code {0}. Please check the errors: \"{1}\"".format(response.status_code, str(response.text)))
    else:
        pass

    return




