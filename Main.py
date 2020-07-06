import spotipy
import yaml
import spotipy.util as util
from MusicGrab import MusicGrab

stream = open("config.yaml") # Opens the config Path
user_config = yaml.safe_load(stream) # Safe Loads using yaml
user_id = user_config['username'] # username

token = util.prompt_for_user_token(user_config['username'], scope='playlist-modify-private,playlist-read-private', client_id=user_config['client_id'], client_secret=user_config['client_secret'], redirect_uri=user_config['redirect_uri']) # Generates a token
sp = spotipy.Spotify(auth=token) # Create a Spotipy Instance

def split_artist(artist,song,sp):
    """We run this function if we found an error while searching for the song and artist in spotify. We check to see if
    this can be solved by formatting the query.
    
    Inputs:
        artist - The artist in text format
        song - The song in text format
        sp - The spotipy instance
    
    Outputs:
        The Spotipy search results
        """

    artist = artist.lower() # Make it lowercase
    artist_mod = artist.split("&")[0]     # Split the string based off the apersand and "and" to remove featuring artists
    artist_mod = artist_mod.split("and")[0]

    query = "artist:{} track:{}".format(artist_mod,song) # Creates a new query
    result = sp.search(q=query, type='track', limit=1) # Searching

    if result['tracks']['total']: # Do any files exist

        return result # Success


    artist_mod = artist.split("/")[0] # Chooses all text before a baclslash
    query = "artist:{} track:{}".format(artist_mod,song) # Generates a new query
    result = sp.search(q=query, type='track', limit=1)

    if result['tracks']['total']:
        return result

    song_mod = song.replace("\'","") # Chooses all text before the quotation ' 
    query = "artist:{} track:{}".format(artist,song_mod)
    result = sp.search(q=query, type='track', limit=1)

    return result # Here we have exhausted all formatting




def convert_to_uri(artist_results):
    """ A function to convert the spotipy searches (usually in a dictionary format) into uri numbers.
    
    Inputs:
        artist_results - A list of spotipy search results
        
    Outputs:
        tracklist - A list of uri's for each song"""

    tracklist = []

    for i in range(len(artist_results)):

        if not artist_results[i]: # Skip failed searches
            continue

        tracklist.append(artist_results[i]['tracks']['items'][0]['uri']) # Finds the uri


    return tracklist


def get_top_songs_for_artist(art_song):
    """ Main search function. Searches spotify using spotipy for the specific artist and song, selects top result.
    Inputs:
        art_song - A list with each element as [artist_name, song_name]
        
    Outputs:
        artist_results - A list with each element containing either None or spotipy search results for the artist and song"""
        
    Failure_Count = 0
    artist_results = [""] * len(art_song) # Creates a blank string list

    for i in range(len(art_song)):


        query = "artist:{} track:{}".format(art_song[i][0],art_song[i][1]) # Creates a query
        artist_results[i] = sp.search(q=query, type='track', limit=1) # Does the searching

        if artist_results[i]['tracks']['total']: # Checks to see if search was successful
        
            print("Success")
            continue # Successful search. Continues to next element


        artist_results[i] = split_artist(art_song[i][0],art_song[i][1],sp) # Error found, attempt to reformat the query


        if artist_results[i]['tracks']['total']: # Check if search was successful
        
            print("Success after split")
            continue # Successful search after reformatting


        print("Failure") # Failed search
        artist_results[i] = None
        Failure_Count+=1


    print("{:.1f}% Rate".format(Failure_Count/len(art_song) * 100)) # Prints failure rate of the total list
    return artist_results


def Playlist_Id(name):
    """ A function that will find the playlist id of the users personal playlist
    Inputs:
        name - The name in text of the users spotify playlist
        
    Outputs:
        my_playlist_id - The id of the playlist"""

    UsrPlists=sp.current_user_playlists()
    PlistFound = False

    for PlistIndex in range(len(UsrPlists['items'])):

        if UsrPlists['items'][PlistIndex]['name'] == name: # Checks if the playlist corresponds to the name given
            print("Playlist Found")
            PlistFound = True
            break

    if not PlistFound: # Raises error if playlist name is not found in current user playlists.
        raise Exception("Playlist Not Found! Check playlist name is correct.")

    my_playlist_id = UsrPlists['items'][PlistIndex]['id']
    return my_playlist_id



personal_playlist_name = user_config["personal_playlist_name"] # The name of the users personal spotify playlist to overwrite and save the songs to
my_playlist_id = Playlist_Id(personal_playlist_name)  # Gets the playlist id from the name


Artist_Songs = MusicGrab(url = user_config["radio_url"]) # Obtains the music songs from onlineradiobox
artist_results = get_top_songs_for_artist(Artist_Songs) # Obtain spotipy searches from the artist_song list
tracklist = convert_to_uri(artist_results) # Obtain song uri's from the spotipy searches



sp.user_playlist_replace_tracks(user_id,my_playlist_id,[]) # Clear the playlist

chunk_size = 99 # Spotify can only accept 100 tracks
for i in range(0, len(tracklist), chunk_size):
    print("Adding chunk",int(i/chunk_size)+1)
    chunk = tracklist[i:i+chunk_size] # Designate the chunk
    sp.user_playlist_add_tracks(user_id,my_playlist_id,chunk,position = i) # Add the uri tracks to the spotipy playlist



