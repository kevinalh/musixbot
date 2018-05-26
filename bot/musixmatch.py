from django.conf import settings

from .models import MxmTrack

import requests


class MxmResponse:
    """
    Response from Musixmatch to a query.
    """
    def __init__(self, response):
        try:
            # We unpack the response
            self.status = int(response['message']['header']['status_code'])
            tracks = response['message']['body']['track_list']
            self.tracks = []
            for index in range(len(tracks)):
                track, _ = MxmTrack.objects.get_or_create_track(tracks[index]['track'])
                self.tracks.append(track)
            self.index = len(self.tracks)
        except KeyError:
            raise ValueError("The response is not of the correct format.")

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.tracks[len(self.tracks) - self.index + 1]


def track_search(lyrics):
    mxm_url = settings.MUSIXMATCH_ENTRY + "track.search"
    data = {
        'q': lyrics,
        's_track_rating': 'desc',
        'apikey': settings.MUSIXMATCH_KEY
    }
    try:
        response = requests.get(mxm_url, params=data, timeout=1)
    except requests.exceptions.ConnectionError:
        response = {
            'message': {
                'header': {'status_code': 500},
                'body': {'track_list': []}
            }
        }
        return MxmResponse(response)
    else:
        return MxmResponse(response.json())


