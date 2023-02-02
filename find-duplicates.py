import csv
import os
import re
import collections

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials


# custom method to ensure playlist isn't capped at 100 songs
# keeps going to next page of playlist until the end
def get_playlist_tracks(playlist_uri):
    results = session.playlist_tracks(playlist_uri)
    tracks = results['items']
    while results['next']:
        results = session.next(results)
        tracks.extend(results['items'])
    return tracks

# load credentials from .env file
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")

# prompt user for link
print("Enter your playlist link")
PLAYLIST_LINK = input()
print()

# authenticate
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)

# create spotify session object
session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# get uri from https link
if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", PLAYLIST_LINK):
    playlist_uri = match.groups()[0]
else:
    raise ValueError("Expected format: https://open.spotify.com/playlist/...")

# get list of tracks in a given playlist 
tracks = get_playlist_tracks(playlist_uri)

items = []
for track in tracks:
    name = track["track"]["name"]
    artist = ", ".join(
        [artist["name"] for artist in track["track"]["artists"]]
    )

    name_and_artist = (name, artist)
    items.append(name_and_artist)


duplicates = list(set([ele for ele in items
                if items.count(ele) > 1]))

if len(duplicates) == 0:
    print("There are no duplicates in this playlist")
else:
    print("The duplicates in your playlist are: ")
    for x in range(len(duplicates)):
        print(duplicates[x][0] + ", " + duplicates[x][1])
