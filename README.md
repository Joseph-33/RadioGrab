# RadioGrab

Do you love listening to the radio?

Are you sick of radio DJ's who won't stop talking?

Look no further, this python script will make a  spotifyplaylist out of the last 24h of songs played on the radio.

# Getting Started
- Edit the config.yaml file with a text editor and fill in the required values
- Run Main.py using python3
- Once Main.py is run, a browser should open, follow the instructions in the console

# Prequisites
- An internet connection
- Spotify Premium
- Python 3.x
  - [Spotipy](https://pypi.org/project/spotipy/)
  - [html2text](https://pypi.org/project/html2text/)
  - [Yaml](https://pypi.org/project/PyYAML/)

# How to obtain a client and secret id
1. [Create a new app in spotify dashboard](https://developer.spotify.com/dashboard/applications)
2. Locate your apps client id and secret
3. Set your app redirect uri to `http://127.0.0.1`

More help [here](https://developer.spotify.com/documentation/general/guides/authorization-guide/) and [here](https://spotipy.readthedocs.io/en/2.12.0/#authorization-code-flow)

# Installing/Running
Use git clone to download repository
```
git clone https://github.com/Joseph-33/RadioGrab.git
```
Input all your spotify details into the config.yaml

Create a spotify playlist (it can be public private or collaborative), place the name of the playlist into the config.yaml

Input your desired radio station and start time into the config.yaml

run the script with

```
python Main.py
```



# Authors
- Joseph Andrews


