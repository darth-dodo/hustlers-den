import os
import sys
import logging


def generate_knowledge_store_published_message(knowledge_store_object):
    """
    Util for creating knowledge store message
    :param knowledge_store_object: KnowledgeStore object
    :return: str
    """
    hustler_name = knowledge_store_object.created_by.first_name if knowledge_store_object.created_by.first_name \
        else knowledge_store_object.created_by.email
    resource_name = knowledge_store_object.name
    resource_url = knowledge_store_object.url
    categories = list(knowledge_store_object.categories.values_list('name', flat=True))

    message = "{0}".format(resource_name)

    if resource_url:
        message = "{0} ({1})".format(message, resource_url)

    if categories:
        categories_str = ', '.join(categories)
        message = "{0} across categories *{1}*".format(message, categories_str)

    if hustler_name:
        message = "{0} has been posted by {1}".format(message, hustler_name)

    return message
