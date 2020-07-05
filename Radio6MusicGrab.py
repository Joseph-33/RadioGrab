import urllib.request
import html2text
import re

def Radio6MusicGrab(url="https://onlineradiobox.com/uk/bbcradio6/playlist/1?cs=uk.bbcradio6"):
    """"A function used to grab all the recent songs from online radiobox.
    Inputs:
        None
    
    Outputs:
        Approximately 143 songs in a list with each element of the format [artist,song]"""
    #url = "https://onlineradiobox.com/uk/jackfmsurrey/playlist/1?cs=uk.jackfmsurrey"

    with urllib.request.urlopen(url) as link:
        html = link.read().decode("utf8")
    
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
    text_split_by_line = re.split("\d{2}:\d{2}\s\|",text)[1:] # Skips the first line as it's not great
    Simple_Counter = 0
    Final_list = []
    for line in text_split_by_line[1:]:

        Simple_Counter += 1
        artist, song = re.split(" - ",line)[:2] # Obtain the and the song from a split by the tilde, notice the space

        artist = artist.split(",")[0] # For artists only, only take everything before the first comma, to screen for featuring artists
        artist = artist.strip() # Strip leading and trailing whitespace
        song = song.strip() # Remove leading and trailing whitespace

        Final_list.append([artist,song])
    return(Final_list)



if __name__ == "__main__":
    artists_songs = Radio6MusicGrab()
