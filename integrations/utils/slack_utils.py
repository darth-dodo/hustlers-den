import os
import sys
import logging
import json
import requests

from integrations.constants import SLACK_WEBHOOK_CHANNEL_URL, SLACK, ACTIVE_BROADCAST_CHANNELS


logger = logging.getLogger(__name__)


def post_message_to_slack_channel(message):
    """
    Send a message to a particular slack channel using the webhook
    
    TODO Register the message to BroadcastMessage model on successful delivery
     
     :param message: `str`
     :return: None
    
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


def trigger_knowledge_store_broadcast_activity(knowledge_store_object_id, broadcast_channels=[]):
    """
    
    Wrapper method to broadcast knowledge store across several channels
    
    TODO: hook it up with the BroadcastMessage model to prevent sending same resource broadcast multiple number of times
    
    :param knowledge_store_object_id: KnowledgeStore object
    :param broadcast_channels: List of broadcast channels
    :return: None

    """

    logger.debug("Data {0} ".format(locals()))

    # validations
    if not broadcast_channels:
        logger.warning("No broadcast channel provided")
        return

    if not isinstance(broadcast_channels, list):
        logger.warning("Incompatible broadcast channel format provided")
        return

    if not set(broadcast_channels).issubset(set(ACTIVE_BROADCAST_CHANNELS)):
        logger.warning("Incorrect broadcast channel provided")
        return

    from knowledge.models import KnowledgeStore
    try:
        knowledge_store_obj = KnowledgeStore.objects.get(id=knowledge_store_object_id)
    except KnowledgeStore.DoesNotExist:
        logger.error("Knowledge store object does not exist")
        return

    # creating the broadcast message
    broadcast_message = knowledge_store_obj.knowledge_store_published_message

    if SLACK in broadcast_channels:
        post_message_to_slack_channel(message=broadcast_message)

    return

