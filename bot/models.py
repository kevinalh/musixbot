from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist

import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
<<<<<<< HEAD
=======
from typing import Dict, List
>>>>>>> dev

from .utils import sp_treat_string


# This is the URL for the messages API
FB_URL = settings.MESSAGES_ENTRY + '?access_token=' + settings.PAGE_TOKEN

# Spotify object
client_manager = SpotifyClientCredentials(client_id=settings.SPOTIFY_CLIENT_ID,
                                          client_secret=settings.SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_manager)


class TrackManager(models.Manager):

    def get_or_create_track(self, data: Dict):
        created = False
        try:
            track = MxmTrack.objects.get(commontrack_id=data['commontrack_id'])
        except ObjectDoesNotExist:
            track = self.create_track(data)
            created = True
        return track, created

    def create_track(self, data: Dict):
        try:
            commontrack_id = data['commontrack_id']
            artist_name = data['artist_name']
            track_name = data['track_name']
            artist_id = data['artist_id']
            album_id = data['album_id']
            album_name = data['album_name']
            track_url = data['track_share_url']
            try:
                vanity_id = data['commontrack_vanity_id']
            except KeyError:
                vanity_id = artist_name + " - " + track_name

            # For some reason, the image URL in the queries is always a default no-cover URL.
            # Otherwise, the code would be as follows:
            #   image_url = data['album_coverart_100x100']
            # We could scrape the website but this is against the API terms
            # (https://about.musixmatch.com/apiterms/)
            # So we're going to use the Spotify API
            image_url = data['album_coverart_100x100']
            spotify_url = None
            sp_string = sp_treat_string(artist_name, track_name)
            try:
                sp_track = sp.search(sp_string, limit=1)
            except spotipy.client.SpotifyException as e:
                print(e)
            else:
                sp_track = sp_track['tracks']['items']
                if len(sp_track) > 0:
                    sp_track = sp_track[0]
                    spotify_url = sp_track['preview_url']
                    if len(sp_track['album']['images']) > 0:
                        if image_url == 'http://s.mxmcdn.net/images-storage/albums/nocover.png':
                            image_url = sp_track['album']['images'][0]['url']

            track = MxmTrack(commontrack_id=commontrack_id,
                             artist_name=artist_name,
                             track_name=track_name,
                             artist_id=artist_id,
                             album_id=album_id,
                             image_url=image_url,
                             track_url=track_url,
                             spotify_url=spotify_url,
                             album_name=album_name,
                             vanity_id=vanity_id)
            track.save()
            return track
        except (ValidationError, KeyError, AttributeError) as e:
            print(e)
            raise ValueError("The data doesn't have the form of a track.")


class MessageManager(models.Manager):

    def create_message(self, query: Dict):
        # We check this for all Facebook webhook events.
        if query.get('object') != 'page':
            raise ValueError("The request doesn't have object=page as an attribute.")

        # The actual messaging object as specified by the API.
        # Note that the API specification guarantees that this list has only one element.
        [messaging] = query['entry'][-1]['messaging']
        # Use the information for creating the MessageEvent.
        psid = messaging['sender']['id']
        # Get or create the sender for this message.
        sender, _ = BotUser.objects.get_or_create(psid=str(psid))

        if 'message' in messaging:
            # The actual text of the message
            message_text = messaging['message']['text']
            if message_text[0] == "/":
                # It's a command
                event = MessageEvent(text=message_text, sender=sender, type=MessageEvent.COMMAND)
            else:
                # It's not a command but lyrics
                event = MessageEvent(text=message_text, sender=sender, type=MessageEvent.LYRICS)
            event.save()
        elif 'postback' in messaging:
            # We're dealing with a favorite button press
            commontrack_id = messaging['postback']['payload']
            try:
                track = MxmTrack.objects.get(commontrack_id=commontrack_id)
            except ObjectDoesNotExist as e:
                print(e)
                raise ValueError
            else:
                event = MessageEvent(text="", sender=sender, related_track=track,
                                     type=MessageEvent.FAVORITE)
                event.save()

        return event


class MxmTrack(models.Model):
    """
    A Musixmatch track object.
    """
    commontrack_id = models.PositiveIntegerField(primary_key=True)
    track_name = models.TextField()
    artist_name = models.TextField()
    vanity_id = models.TextField()
    album_id = models.PositiveIntegerField()
    album_name = models.TextField()
    artist_id = models.PositiveIntegerField()
    image_url = models.URLField(null=True, max_length=500)
    track_url = models.URLField(default='https://www.musixmatch.com/', max_length=500)
    spotify_url = models.URLField(null=True, max_length=500)

    objects = TrackManager()

    def messenger_track(self, user):
        """
        :return: A dictionary in the Facebook-required template form.
        """
        msg = {
            'title': str(self.artist_name) + " - " + str(self.track_name),
            'image_url': str(self.image_url),
            'subtitle': str(self.album_name),
            'default_action': {
                'type': 'web_url',
                'url': str(self.track_url),
                'messenger_extensions': 'false',
                'webview_height_ratio': 'tall'
            }
        }
        try:
            if not user.favorites.filter(commontrack_id=self.commontrack_id).exists():
                # If the user hasn't checked the song as a favorite, show the button
                msg['buttons'] = [{
                    'type': 'postback',
                    'title': 'Favorite',
                    'payload': str(self.commontrack_id)
                }]
        except Exception as e:
            print(e)
        return msg

    def __str__(self):
        return str(self.artist_name) + " - " + str(self.track_name)


class BotUser(models.Model):
    """
    A user in the database.
    """
    psid = models.TextField(unique=True)
    favorites = models.ManyToManyField(MxmTrack)

    def _build_message(self):
        msg = {
            'recipient': {'id': self.psid}
        }
        return msg

    def _send(self, msg):
        # Use the API and save the response in a variable
        requests.post(FB_URL, json=msg)

    def send_action(self, action):
        msg = self._build_message()
        msg['sender_action'] = action
        self._send(msg)

    def send_text(self, text):
        msg = self._build_message()
        msg['message'] = {'text': text}
        msg['messaging_type'] = 'RESPONSE'
        self._send(msg)

    def send_list_tracks(self, tracks: List[MxmTrack]):
        msg = self._build_message()
        msn_tracks = [track.messenger_track(self) for track in tracks]
        msg['message'] = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'sharable': 'true',
                    'elements': msn_tracks
                }
            }
        }
        self._send(msg)

    def favorites_text(self):
        msg = "These are your favorite songs:\n"
        for favorite in self.favorites.all():
            msg += "- " + str(favorite) + "\n"
        return msg

    def __str__(self):
        return self.psid


class MessageEvent(models.Model):
    """
    A message sent by a user to the server.
    """
    LYRICS = 'LY'
    FAVORITE = 'FA'
    COMMAND = 'CO'
    MESSAGE_TYPES = (
        (LYRICS, 'Lyrics'),
        (COMMAND, 'Command'),
        (FAVORITE, 'Favorite')
    )

    text = models.TextField()
    type = models.CharField(max_length=2, choices=MESSAGE_TYPES, default=LYRICS)
    sender = models.ForeignKey('BotUser', on_delete=models.CASCADE)
    related_track = models.ForeignKey(MxmTrack, null=True, blank=True, on_delete=models.SET_NULL)

    # Custom manager
    objects = MessageManager()

    def __str__(self):
        return self.text


def stats_text():
    msg = "Stats:\n"
    msg += "Number of users: " + str(BotUser.objects.all().count()) + "\n"
    return msg
