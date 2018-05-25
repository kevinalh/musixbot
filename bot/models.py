from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import requests

from typing import Dict


# This is the URL for the messages API
FB_URL = settings.MESSAGES_ENTRY + '?access_token=' + settings.PAGE_TOKEN


class TrackManager(models.Manager):

    def get_or_create_track(self, data: Dict):
        track = None
        try:
            track = MxmTrack.objects.get(commontrack_id=data['commontrack_id'])
        except ObjectDoesNotExist:
            track = self.create_track(data)
            track.save()
        return track

    def create_track(self, data: Dict):
        try:
            commontrack_id = data['commontrack_id']
            artist_name = data['artist_name']
            track_name = data['track_name']
            track = MxmTrack(commontrack_id=commontrack_id,
                             artist_name=artist_name,
                             track_name=track_name)
            track.save()
            return track
        except (AttributeError, KeyError, ValueError, ValidationError):
            raise ValueError("The data doesn't have the form of a track.")


class MessageManager(models.Manager):

    def create_message(self, query: Dict):
        # We check this for all Facebook webhook events.
        if query.get('object') != 'page':
            raise ValueError("The request doesn't have object=page as an attribute.")

        try:
            # The actual messaging object as specified by the API.
            [messaging] = query['entry'][-1]['messaging']
            # Use the information for creating the MessageEvent.
            psid = messaging['sender']['id']
            # Get or create the sender for this message.
            sender, _ = BotUser.objects.get_or_create(psid=str(psid))
            # The actual text of the message
            message_text = messaging['message']['text']
            # Build the object
            event = MessageEvent(text=message_text, sender=sender)
            event.save()
            return event
        except (AttributeError, KeyError, ValueError, ValidationError):
            raise ValueError("The request doesn't define a messaging event.")


class BotUser(models.Model):
    """
    A user in the database.
    """
    psid = models.TextField(unique=True)

    def __build_message(self):
        msg = {
            'recipient': {'id': self.psid}
        }
        return msg

    @staticmethod
    def send(msg):
        # Use the API and save the response in a variable
        requests.post(FB_URL, json=msg)

    def send_action(self, action):
        msg = self.__build_message()
        msg['sender_action'] = action
        self.__class__.send(msg)

    def send_message(self, text):
        msg = self.__build_message()
        msg['message'] = {'text': text}
        msg['messaging_type'] = 'RESPONSE'
        self.__class__.send(msg)

    def __str__(self):
        return self.psid


class MessageEvent(models.Model):
    """
    A message sent by a user to the server.
    """
    text = models.TextField()
    sender = models.ForeignKey('BotUser', on_delete=models.CASCADE)

    # Custom manager
    objects = MessageManager()

    def __str__(self):
        return self.text


class MxmTrack(models.Model):
    """
    A Musixmatch track object.
    """
    commontrack_id = models.PositiveIntegerField()
    track_name = models.TextField()
    artist_name = models.TextField()

    objects = TrackManager()

    def __str__(self):
        return str(self.artist_name) + " - " + str(self.track_name)

