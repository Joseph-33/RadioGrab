import spotipy
import yaml
import spotipy.util as util
import datetime
from MusicGrab import music_grab
from SpModules import get_top_songs_for_artist, playlist_id, convert_to_uri, split_artist
from spotipy.oauth2 import SpotifyClientCredentials

stream = open("config.yaml") # Opens the config Path
user_config = yaml.safe_load(stream) # Safe Loads using yaml
user_id = user_config['username'] # Spotify Username
personal_playlist_name = user_config["personal_playlist_name"] # The name of the users personal spotify playlist to overwrite and save the songs to
start_time = user_config["start_time"] # The first song on the playlist was played on the radio at the start time

if start_time.lower() == "now": # Get the current time for when time config is now.
    start_time_str = str(datetime.datetime.now().time())
    start_time = ":".join(start_time_str.split(":")[:2])

#sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
scope='playlist-modify-private,playlist-read-private,playlist-read-collaborative'
token = util.prompt_for_user_token(user_config['username'], scope=scope, client_id=user_config['client_id'], client_secret=user_config['client_secret'], redirect_uri=user_config['redirect_uri']) # Generates a token
sp = spotipy.Spotify(auth=token) # Create a Spotipy Instance




my_playlist_id = playlist_id(personal_playlist_name,sp)  # Gets the playlist id from the name

artist_songs = music_grab(url = user_config["radio_url"],start_time = start_time) # Obtains the music songs from onlineradiobox
artist_results = get_top_songs_for_artist(artist_songs,sp) # Obtain spotipy searches from the artist_song list
tracklist = convert_to_uri(artist_results) # Obtain song uri's from the spotipy searches




sp.user_playlist_replace_tracks(user_id,my_playlist_id,[]) # Clears the playlist

chunk_size = 99 # Spotify can only accept 100 tracks
for i in range(0, len(tracklist), chunk_size):
    print("Adding chunk",int(i/chunk_size)+1)
    chunk = tracklist[i:i+chunk_size] # Designate the chunk
    sp.user_playlist_add_tracks(user_id,my_playlist_id,chunk,position = i) # Add the uri tracks to the spotipy playlist



