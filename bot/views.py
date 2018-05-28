from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import MessageEvent, stats_text

from .musixmatch import track_search

import json, sys, traceback


@csrf_exempt
def webhook_messenger(request: HttpRequest):
    """
    View that interacts with the Facebook Messenger API.

    A GET method is used to subscribe to the webhook, and POST is used for actual API interaction.
    It is required that the server returns a 200 status code on every request.

    :param request: HttpRequest sent to the server.
    :return: HttpResponse that acknowledges the interaction in case it's well-formed according to
        the API standards.
    """
    response = HttpResponse(status=200, content_type='application/json')
    response.content = 'OK'

    if request.method == 'POST':
        # Responding to a Messenger API request.
        query = json.loads(request.body)

        try:
            event = MessageEvent.objects.create_message(query=query)
        except ValueError as e:
            print(e)
            return response
        else:
            user = event.sender
            # Mark that we've seen the message
            user.send_action('mark_seen')
            # Signal that we are writing a message
            user.send_action('typing_on')

        try:
            if event.type == MessageEvent.LYRICS:
                # Look for the song lyrics
                mxm = track_search(event.text)

                if mxm.status == 200:
                    if len(mxm.tracks) > 0:
                        # At least one track found
                        if len(mxm.tracks) > 10:
                            # Make sure we don't send more than 10 templates to comply with
                            # Facebook's API requirements.
                            mxm.tracks = mxm.tracks[:10]
                        # Send the message to the user
                        user.send_list_tracks(mxm.tracks)
                    else:
                        # No track returned by Musixmatch
                        user.send_text("Couldn't find lyrics.")
                else:
                    # Some error happened while contacting Musixmatch
                    user.send_text("Couldn't contact the lyrics service.")

            elif event.type == MessageEvent.FAVORITE:
                # Set song as favorite
                track = event.related_track
                if user.favorites.filter(commontrack_id=track.commontrack_id).exists():
                    # If song is already saved as favorite, send a message telling that's
                    # the case.
                    user.send_text("\"" + track.track_name + "\" already saved.")
                else:
                    # Otherwise, save the track and send a confirmation message.
                    user.favorites.add(track)
                    user.send_text("\"" + track.track_name + "\" saved as favorite.")

            elif event.type == MessageEvent.COMMAND:
                # The user used a command. For now, only /stat and /fav are implemented.
                if event.text == "/stat":
                    msg = stats_text()
                elif event.text == "/fav":
                    msg = user.favorites_text()
                else:
                    msg = "Try the /stat or /fav commands."
                user.send_text(msg)

        except ValueError as e:
            print(e)
            traceback.print_exc(file=sys.stdout)

        finally:
            # The following response is just to acknowledge the server. It's required!
            response.status_code = 200

    elif request.method == 'GET':
        # Facebook uses a GET for subscription to the webhook.

        # Hard-coded token for verification used by Facebook.
        verify_token = settings.VERIFY_TOKEN
        # Contents of the GET request.
        query = request.GET

        # We now verify the request has the appropriate form.
        if 'hub.mode' in query and 'hub.verify_token' in query:
            mode = query['hub.mode']
            token = query['hub.verify_token']
            challenge = query.get('hub.challenge')

            # Check the mode of the query is subscribe, and whether the token matches.
            if mode == 'subscribe' and token == verify_token:
                # The token matched! Send the challenge back to verify.
                response.content = challenge
                response.status_code = 200
            else:
                # Forbidden: The token didn't match.
                response.status_code = 403

    return response
