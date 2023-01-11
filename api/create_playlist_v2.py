import os
import spotipy #pip install spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv #pip install python-dotenv 
import datetime
import json
load_dotenv()

def login():
    spot_client = os.environ["spotify_client_id"]
    spot_token = os.environ["spotify_token"]
    redirect = os.environ["redirect_uri"]
    scopes = [
        "user-top-read",
        "playlist-read-private",
        "user-top-read"
    ]
    auth_manager = SpotifyOAuth(
        client_id= spot_client,
        client_secret=spot_token,
        redirect_uri= redirect,
        scope=scopes
    )
    
    global spot
    spot = spotipy.Spotify(auth_manager=auth_manager)
    user = spot.me()['id']

    # return print("Current user: {}".format(user))

def recommendations(type,term: str,num_songs: int, valence: int = None):
    #Create playlist based on either the users' top 5 artists or tracks. The "valence" is my target value, 
    #determining the mood of the playlist. The valence will be determined by sentiment analysis.
    if type == "artist":
        top_artists = spot.current_user_top_artists(limit=5,time_range=term)
        artist_dict = {} #Holds all data need for the frontend as well as artist URI for song recommendations
        for artist in top_artists['items']:
            artist_dict[artist['name']] = [artist['images'][0]['url'], artist['uri']] #{"artist name" : ["artist image url", "artist uri"]}
        artist_seeds = [] #Seed used to base your playlist off of
        for items in artist_dict.values():
            artist_seeds.append(items[1])
        
        song_recs = spot.recommendations(seed_artists= artist_seeds,limit= num_songs)
        tracks = {}
        track_num = 0
        for track in song_recs['tracks']:
            tracks[track_num] = track['uri']
            track_num += 1
        current_user = spot.me()['id']
        playlist = spot.user_playlist_create(
            user = current_user ,
            name = "Sentify Playlist",
            public = False,
            description = "Creating playist based on how you feel 😉" )

        spot.playlist_add_items(
            playlist_id= playlist['id'], 
            items = list(tracks.values())
            ) 

        spot.playlist_change_details(playlist_id = playlist['id'], public = False )
        print(playlist['id'])
        # print(song_recs)
        # print(artist_dict)
        # print(tracks)
    elif type == "track":
        top_tracks = spot.current_user_top_tracks(limit=5,time_range=term)
        track_dict = {}

        for track in top_tracks['items']:
            track_dict[track['name']] = track['uri'] #{"track name" : "track uri"}
        track_seeds = [] #Seed used to base your playlist off of
        for item in track_dict.values():
            track_seeds.append(item)

        song_recs = spot.recommendations(seed_tracks= track_seeds, limit= num_songs)
        tracks = {}
        track_num = 0
        for track in song_recs['tracks']:
            tracks[track_num] = track['uri']
            track_num += 1
        current_user = spot.me()['id']
        playlist = spot.user_playlist_create(
            user = current_user ,
            name = "Sentify Playlist",
            public = False,
            description = "Creating playist based on how you feel 😉" )

        spot.playlist_add_items(
            playlist_id= playlist['id'], 
            items = list(tracks.values())
            ) 

        print(playlist['id'])


if __name__ == "__main__":
    login()
    recommendations("track","medium_term",5)