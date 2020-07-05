import spotipy
import yaml
import spotipy.util as util
#from spotipy.oauth2 import SpotifyOAuth
from Radio6MusicGrab import Radio6MusicGrab
ConfigPath = "/home/pi/Documents/Playlists/config.yaml"



stream = open(ConfigPath)
user_config = yaml.safe_load(stream)

user_id = "mojo--3"
token = util.prompt_for_user_token(user_config['username'], scope='playlist-modify-private,playlist-read-private', client_id=user_config['client_id'], client_secret=user_config['client_secret'], redirect_uri=user_config['redirect_uri'])

sp = spotipy.Spotify(auth=token)

def split_artist(artist,song,sp):
    """Here we split the artist and generate a new query and searches with this new query"""

    artist = artist.lower() # Make it lowercase

    artist_mod = artist.split("&")[0]     # Split the string
    artist_mod = artist_mod.split("and")[0]

    query = "artist:{} track:{}".format(artist_mod,song) # Creates a new query

    result = sp.search(q=query, type='track', limit=1) # Does the searching

    if result['tracks']['total']:

        return result


    artist_mod = artist.split("/")[0] # Splits based off the backslash
    query = "artist:{} track:{}".format(artist_mod,song)
    result = sp.search(q=query, type='track', limit=1)

    if result['tracks']['total']:
        return result

    song_mod = song.replace("\'","")
    query = "artist:{} track:{}".format(artist,song_mod)
    result = sp.search(q=query, type='track', limit=1)

    return result




def convert_to_uri(artist_results):

    tracklist = []

    for i in range(len(artist_results)):

        if not artist_results[i]:
            continue

        tracklist.append(artist_results[i]['tracks']['items'][0]['uri'])


    return tracklist


def get_top_songs_for_artist(art_song):
    Failure_Count=0
    artist_results = [""] * len(art_song)

    for i in range(len(art_song)):


        query = "artist:{} track:{}".format(art_song[i][0],art_song[i][1]) # Creates a query

        artist_results[i] = sp.search(q=query, type='track', limit=1) # Does the searching

        if artist_results[i]['tracks']['total']: # Checks to see if search was successful
            print("Success")
            continue


        artist_results[i] = split_artist(art_song[i][0],art_song[i][1],sp)

        if artist_results[i]['tracks']['total']:
            print("Success after split")
            continue


        print("Failure")
        artist_results[i] = None
        Failure_Count+=1


    print("{:.1f}% Rate".format(Failure_Count/len(art_song) * 100))
    return artist_results


def Playlist_Id(name):

    UsrPlists=sp.current_user_playlists()

    for PlistIndex in range(len(UsrPlists['items'])):

        if UsrPlists['items'][PlistIndex]['name'] == name:
            print("Playlist Found")
            break

    my_playlist_id = UsrPlists['items'][PlistIndex]['id']
    return my_playlist_id




my_playlist_id = Playlist_Id("Alrm")


Artist_Songs = Radio6MusicGrab()
artist_results = get_top_songs_for_artist(Artist_Songs)
tracklist = convert_to_uri(artist_results)



sp.user_playlist_replace_tracks(user_id,my_playlist_id,[]) # Empty the playlist

chunk_size = 99 # Spotify can only accept 100 tracks
for i in range(0, len(tracklist), chunk_size):
    print("Adding chunk",int(i/chunk_size)+1)
    chunk = tracklist[i:i+chunk_size]
    sp.user_playlist_add_tracks(user_id,my_playlist_id,chunk,position = i)



