import string


def sp_treat_string(artist: str, track: str):
    """
    Takes two strings, for artist name and track name, and returns a string that
    Spotify will easily search in its database.
    """
    try:
        artist = artist.split("feat", 1)[0]
        artist = artist.split("(", 1)[0]
        artist = artist.split("[", 1)[0]
        artist = artist.split(",", 1)[0]
        track = track.split("(", 1)[0]
        track = track.split("[", 1)[0]
        track = track.split("-", 1)[0]
    except IndexError:
        pass
    # Remove all punctuation from the track name
    for char in string.punctuation:
        track = track.replace(char, ' ')
    return artist + " " + track
