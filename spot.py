import spotipy
import spotipy.util as util
import os
import json
import datetime
from datetime import date
import time
from Track import Track
from settings import CLIENT_SECRET, USERNAME, CLIENT_ID

path = 'user_playing_history.json'
b = ['']
track_list = []
progress_ms_prev = 0
track_id_prev = ""


def spotify_connection():  # Spotify Authorization
    token = util.prompt_for_user_token(username=USERNAME,
                                       scope='user-read-currently-playing ',
                                       client_id=CLIENT_ID,
                                       client_secret=CLIENT_SECRET,
                                       redirect_uri='http://localhost:8888/callback')
    sp = spotipy.Spotify(auth=token)
    return sp


def add_tracks_to_list():  # Parsing the JSON file and then adding the most played tracks by count criterion to a list
    with open(path, 'r') as json_file:
        json_data = json.load(json_file)
    for i in json_data:
        if i['count'] > 2 and i['track_id'] not in track_list:
            track_list.append(i['track_id'])
            print(track_list)


def create_playlist_with_favorite_tracks():  # Creating playlist to spotify
    a = 'Most played tracks ' + datetime.date.today().strftime('%d-%m-%y')
    sp = spotify_connection()
    sp.user_playlist_create(USERNAME, a, public=True, description='Favorite')
    nn = sp.user_playlists(USERNAME)
    for playlist in nn['items']:  # Parsing playlists
        if playlist['name'] == a:  # Check if playlist exists
            sp.user_playlist_add_tracks(USERNAME, playlist['id'], track_list, position=None)  # Add tracks to playlist


def get_current_track(now_playing):  # Get current user playing track
    artists = []
    progress_ms = now_playing['progress_ms']
    global progress_ms_prev
    global track_id_prev
    if now_playing:
        track_name = now_playing['item']['name']
        if track_name == "":
            return None
        with open(path, 'r') as json_file:  # Reading JSON file
            json_data = json.load(json_file)
        time.sleep(2)
        if now_playing['item']['id'] == track_id_prev:  # Check is current track id is the same with previous
            print(str(progress_ms_prev) + ">" + str(progress_ms))
            if progress_ms_prev > progress_ms:  # Check if the same song is repeated
                print(now_playing['progress_ms'])
                for json_i in json_data:
                    if now_playing['item']['id'] == json_i['track_id']:  # Check if the song is in the JSON
                        json_i['count'] = json_i['count'] + 1  # If song exists count+1 in JSON
                        with open(path, 'w') as file:  # Write to JSON new data
                            json.dump(json_data, file, indent=2)
                        break
            progress_ms_prev = progress_ms
        else:  # else current track id is different with previous track
            track_id_prev = now_playing['item']['id']
            progress_ms_prev = 0
            print(progress_ms_prev)
            for json_i in json_data:  # Parsing JSON
                if now_playing['item']['id'] == json_i['track_id']:  # If current id is in File count+1
                    json_i['count'] = json_i['count'] + 1
                    with open(path, 'w') as file: # Write to JSON new data
                        json.dump(json_data, file, indent=2)
                        break
            else:  # if current id doesn't exist in file write new track to file
                count = 1
                track_id = now_playing['item']['id']
                album_name = now_playing['item']['album']['name']
                temp_artists = now_playing['item']['artists']
                played_date = datetime.datetime.now()
                played_date = str(played_date)
                external_url = now_playing['item']['external_urls']['spotify']
                thumbnail = now_playing['item']['album']['images'][0]['url']
                print(played_date)
                for artist in temp_artists:
                    artists.append(artist['name'])

                track = Track(
                    count=count,
                    name=track_name,
                    track_id=track_id,
                    artists=artists,
                    album=album_name,
                    played_date=played_date,
                    external_url=external_url,
                    thumbnail=thumbnail
                )
                track_as_dict = track.get_track_as_dict()
                return track_as_dict


def write_track_to_file(now_playing):  # Running get_current_track function and writing only new tracks to JSON file
    track_as_dict = get_current_track(now_playing)
    exists = os.path.isfile(path)
    if exists:
        if track_as_dict is not None:
            with open(path) as tracklist:
                tracks = json.load(tracklist)
                tracks.append(track_as_dict)
            with open(path, mode='w') as f:
                f.write(json.dumps(tracks, indent=2))
    else:
        with open(path, mode='w') as f:
            json.dump([], f)


def main():
    while True:
        sp = spotify_connection()
        now_playing = sp.current_user_playing_track()
        today = str(date.today())
        add_tracks_to_list()  # Run function to add most popular songs to list
        if now_playing['is_playing']:  # Only if spotify playing track running the functions
            write_track_to_file(now_playing)
        if today == '2019-11-21' and len(track_list) != 0:  # Set the date to stop script and make playlist
            create_playlist_with_favorite_tracks()
            print('Your tracks have been saved successfully')
            break


if __name__ == "__main__":
    main()