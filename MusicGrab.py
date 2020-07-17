# Imports the necessary libraries
import urllib.request
import html2text
import re
import random

def time_start(text,text_split,start_time):
    """ A function to manage the playlist start time and to create a new rolled list out of it
    
    Inputs:
        text - Readable html text
        start_time - Time in 24h HH:MM of when the first song on the playlist should have been played on the radio
        text_split - text split upon the times in 24h HH:MM format.
    
    Outputs:
        text_split_rolled - A new text_split to accomodate the new start_time"""

    time_list = re.findall("\d{2}:\d{2}",text) # Get all times in format HH:MM from the html text
    time_list.reverse() # Reverse the list, so the times are in ascending order    
    
    time_list_minutes = [int(tstring.split(":")[0]) * 60 + int(tstring.split(":")[1]) for tstring in time_list] # Convert time_list to minutes
    start_time_minutes = int(start_time.split(":")[0]) * 60 + int(start_time.split(":")[1]) # Convert start_time to minutes

    min_value = min(time_list_minutes, key=lambda x:abs(x-start_time_minutes)) # Min function to find the value in time_list closest to start_time
    rolling_index = time_list_minutes.index(min_value) # Calculate index of element in time_list to start_time
    text_split_rolled = text_split[rolling_index:] + text_split[:rolling_index] # Adjust the list to accomodate this.
    
    return text_split_rolled
    

def music_grab(url="https://onlineradiobox.com/uk/bbcradio6/playlist/1?cs=uk.bbcradio6&useStationLocation=1", start_time = "7:30"):
    
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
    text = text.replace("---|---","")
    
    end_index = text.find("Install the free Online Radio Box")
    text = text[:end_index] # Slice the string at the end

    text = text.replace("\n"," ") # Removes all newlines
    text = re.sub("\(.*?\)","",text) # Removes everything in a bracket
    text = re.sub("[\[\]]","",text) # Removes all square brackets
    text = re.sub("\s{2,}"," ",text) # Replaces multiple whitespaces    
    
    text_split = re.split("\d{2}:\d{2}\s\|",text)[1:] # Splits the text into a list every time a time format HH:MM is observed.
    text_split.reverse() # Reverse the list 
    
    
    if start_time.lower() == "random":
        text_split_rolled = random.sample(text_split,len(text_split)) # Shuffle the list
    else:
        text_split_rolled = time_start(text,text_split,start_time) # Call the time_start function
    
    Final_list = [] # Declare our Final list at the beginning
    for line in text_split_rolled: # Start a for loop and loop around each element in our list

        artist, song = re.split(" - ",line)[:2] # Obtain the and the song from a split by the tilde, notice the spaces
        
        artist = artist.split(",")[0] # For artists only, only take everything before the first comma, to screen for featuring artists
        artist = artist.strip() # Strip leading and trailing whitespace
        song = song.strip() # Remove leading and trailing whitespace

        Final_list.append([artist,song])
    return(Final_list)



if __name__ == "__main__": # Check that the file is being directly called
    artists_songs = music_grab()
    a=artists_songs
