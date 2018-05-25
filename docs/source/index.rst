Musixbot
==============

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Musixbot is a chat bot that searches for song lyrics using the Musixmatch API.

Musixmatch API
----------------

When doing a query to the
`Musixmatch API <https://developer.musixmatch.com/documentation/music-meta-data>`_
, we're interested in the Track object, in particular the ``commontrack_id`` attribute,
as this is the unique ID that identifies a song, even on different albums.
We can even use this as the primary key for simplicity.

The API method we're interested in is ``track_search``.

Every call requires the ``apikey`` parameter, and in our case, we'll use the
``q_lyrics`` parameter. This way, calls will be of the form::

    https://api.musixmatch.com/ws/1.1/track.search?q_lyrics=<LYRICS>&apikey=<KEY>

We can also use ``s_track_rating=desc`` for getting the tracks in descending popularity
order.

The result is of the following form::

    {
       "message":{
          "header":{
             "status_code":200,
             "execute_time":0.014848947525024,
             "available":5
          },
          "body":{
             "track_list":[
                {
                   "track":{
                      "track_id":105392428,
                      "track_name":"Pictures Of Me",
                      "track_rating":75,
                      "commontrack_id":10779,
                      "num_favourite":22,
                      "lyrics_id":17053067,
                      "subtitle_id":17833562,
                      "album_id":22659155,
                      "album_name":"Either\/Or",
                      "artist_id":39,
                      "artist_name":"Elliott Smith",
                      "album_coverart_100x100":"http:\/\/s.mxmcdn.net\/images-storage\/albums\/nocover.png",
                      "album_coverart_350x350":"",
                      "album_coverart_500x500":"",
                      "album_coverart_800x800":"",
                      "track_share_url":"https:\/\/www.musixmatch.com\/lyrics\/Elliott-Smith\/Pictures-of-Me?utm_source=application&utm_campaign=api&utm_medium=",
                      "commontrack_vanity_id":"Elliott-Smith\/Pictures-of-Me",
                      "restricted":0,
                      "first_release_date":"1997-02-25T00:00:00Z",
                      "primary_genres":{
                         "music_genre_list":[
                            {
                               "music_genre":{
                                  "music_genre_id":20,
                                  "music_genre_parent_id":34,
                                  "music_genre_name":"Alternative",
                                  "music_genre_name_extended":"Alternative",
                                  "music_genre_vanity":"Alternative"
                               }
                            }
                         ]
                      },
                      "secondary_genres":{
                         "music_genre_list":[
                            {
                               "music_genre":{
                                  "music_genre_id":21,
                                  "music_genre_parent_id":34,
                                  "music_genre_name":"Rock",
                                  "music_genre_name_extended":"Rock",
                                  "music_genre_vanity":"Rock"
                               }
                            },
                            {
                               "music_genre":{
                                  "music_genre_id":10,
                                  "music_genre_parent_id":34,
                                  "music_genre_name":"Singer\/Songwriter",
                                  "music_genre_name_extended":"Singer\/Songwriter",
                                  "music_genre_vanity":"Singer-Songwriter"
                               }
                            }
                         ]
                      }
                   }
                }
             ]
          }
       }
    }

Messenger API
--------------

The Page-scoped ID (PSID) is assigned by the Messenger platform to each user that interacts
with the bot. This is included in the ``sender.id`` field, and should be included in the
``recipient.id`` field when sending messages.

To use the API, we need to
`setup the Webhook <https://developers.facebook.com/docs/messenger-platform/getting-started/webhook-setup>`_.
This requires a SSL certificate.

The app is *required* to respond with a ``200 OK`` response for every webhook event. Otherwise,
it might get unsubscribed.

On subscription to the ``messages`` callback, the webhook will receive messages of the form::

    {
      "sender":{
        "id":"<PSID>"
      },
      "recipient":{
        "id":"<PAGE_ID>"
      },
      "timestamp":1458692752478,
      "message":{
        "mid":"mid.1457764197618:41d102a3e1ae206a38",
        "text":"hello, world!",
      }
    }

.. automodule:: bot
    :members:
    :undoc-members:
.. autofunction:: bot.views.webhook_messenger

Indices and tables
===================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
