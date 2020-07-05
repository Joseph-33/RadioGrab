# Imports the necessary libraries
import urllib.request
import html2text
import re

def MusicGrab(url="https://onlineradiobox.com/uk/bbcradio6/playlist/1?cs=uk.bbcradio6"):
    
    """"A function used to grab all recently played songs from a particular radio station on the website onlineradiobox.
    Inputs:
        url - The url from onlineradiobox 
    
    Outputs:
        List - A list with each element comprising of [arist_name,song_name]
        
    """


    with urllib.request.urlopen(url) as link:
        html = link.read().decode("utf8") # Downloads the html and decodes it
    
    text = html2text.html2text(html) # Makes it readable

    start_index = text.find("---|---")
    text = text[start_index:] # Slice the string at the start.

    end_index = text.find("Install the free Online Radio Box")
    text = text[:end_index] # Slice the string at the end

    text = text.replace("\n"," ") # Removes all newlines
    text = re.sub("\(.*?\)","",text) # Removes everything in a bracket
    text = re.sub("[\[\]]","",text) # Removes all square brackets
    text = re.sub("\s{2,}"," ",text) # Replaces multiple whitespaces


    #print(text)
    text_split = re.split("\d{2}:\d{2}\s\|",text)[1:] # Splits the text into a list every time a time format HH:MM is observed. Also skips first element 
    Final_list = [] # Declare our Final list at the beginning
    for line in text_split[1:]: # Start a for loop and loop around each element in our list


        artist, song = re.split(" - ",line)[:2] # Obtain the and the song from a split by the tilde, notice the spaces

        artist = artist.split(",")[0] # For artists only, only take everything before the first comma, to screen for featuring artists
        artist = artist.strip() # Strip leading and trailing whitespace
        song = song.strip() # Remove leading and trailing whitespace

        Final_list.append([artist,song])
    return(Final_list)



if __name__ == "__main__": # Check that the file is being directly called
    artists_songs = MusicGrab()
