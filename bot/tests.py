from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings

import responses


class WebhookTests(TestCase):
    def setUp(self):
        self.webhook = reverse("bot-webhook")
        self.default_event = {
            'object': 'page',
            'entry': [{'messaging': []}]
        }
        # Setup the mock responses
        self.mock_url = settings.MESSAGES_ENTRY + '?access_token=' + settings.PAGE_TOKEN
        responses.add(responses.POST, self.mock_url, status=200,
                      json={"recipient_id": "125447777",
                            "message_id": "mid.$cAAa-4cvO"})

    def create_message_event(self, messaging):
        """
        Creates a message event given a message object.
        """
        event = {**self.default_event}
        event['entry'][-1]['messaging'].append(messaging)
        return event

    def test_validation(self):
        """
        On a GET request with the appropriate form, the server should return the challenge
        and a 200 status code.
        """
        challenge = "challenge-string"
        data = {
            'hub.mode': 'subscribe',
            'hub.verify_token': settings.VERIFY_TOKEN,
            'hub.challenge': challenge
        }
        c = Client()
        response = c.get(self.webhook, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.content, 'utf-8'), challenge)

    @responses.activate
    def test_simple_message(self):
        """
        On a very simple small message, the server should at least acknowledge by sending
        a 200 status code.
        """
        messaging = {
            'sender': {'id': '1331235'},
            'recipient': {'id': '1111111'},
            'message': {'text': 'Hello world.'}
        }
        event = self.create_message_event(messaging)
        c = Client()
        response = c.post(self.webhook, data=event, content_type='application/json')
        self.assertEqual(response.status_code, 200)
