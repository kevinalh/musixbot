from typing import Dict
from .models import BotUser


class MessageEvent:
    """
    Events received via webhook from the Facebook API.
    """

    def __init__(self, query: Dict):
        # We check this for all Facebook webhook events.
        if query.get('object') != 'page':
            raise ValueError("The request doesn't have object=page as an attribute.")

        try:
            # The actual messaging object as specified by the API.
            [messaging] = query['entry'][-1]['messaging']
            # Encapsulate the information in the class instance.
            psid = messaging['sender']['id']
            self.sender, created = BotUser.objects.get_or_create(psid=str(psid))
            self.message_text = messaging['message']['text']
        except (AttributeError, KeyError, ValueError):
            raise ValueError("The request doesn't define a messaging event.")

    def __str__(self):
        return str(self.sender.psid) + ": " + self.message_text
