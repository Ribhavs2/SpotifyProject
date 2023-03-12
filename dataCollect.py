import json
import requests
from personal import spotify_user_id
from playlist_ids import gym_playlist_id, spark_playlist_id, hindi_playlist_id, sleep_playlist_id, night_playlist_id
from datetime import date
from refresh import Refresh
import pandas as pd
import sys


class LoadPlaylist:
    def __init__(self, playlist_id = gym_playlist_id, spotify_token = ""):
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token
        self.playlist_id = playlist_id
        self.tracks_id = ""
        self.new_playlist_id = ""
        

    def find_songs(self, limit=100, offset = 0):

        # might rename find_songs with somethin like loading_songs
        print("Loading songs from playlist:" + self.playlist_id + " ----")
        #Loop through playlist tracks and add to list
        query = "https://api.spotify.com/v1/playlists/{}/tracks?limit={}&offset={}".format(
            self.playlist_id, limit, offset) #just changed playlist_id to self.playlist_id
        
        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})
        if response.ok:
            print("-----------------------Successfully loaded songs from playlist-----------------------")
        else:
            print("-----------------------Error while loading songs from playlist-----------------------")
            print("Exiting program")
            sys.exit()

        response_json = response.json()
        print("Response:", response)
        #print("LIMIT:", response_json['limit'])

        self.tracks_id = ""
        for j in response_json["items"]:
            self.tracks_id += (j["track"]["id"] + ",") # to make a comma separated list
        self.tracks_id = self.tracks_id[:-1] #to remove last comma that will be added at end
        # print(self.tracks_id)

        #self.add_to_playlist()

    
    def info_extraction(self, iter = 1):
        # extracts all info of each track
        info_list = []
        for i in range(iter):
            print("Calling find_songs to get track_ids of songs in playlist...")
            self.find_songs(limit=100, offset=i*100)

            if(self.tracks_id == ""):
                print("End of playlist reached")
                print("Creating DataFrame with song info")
                break
            else:
                print("Extracting info from track ids...")
                #print(self.tracks_id)
                query = "https://api.spotify.com/v1/audio-features?ids={}".format(self.tracks_id)
                response = requests.get(query, 
                                        headers={"Content-Type": "application/json",
                                                "Authorization": "Bearer {}".format(self.spotify_token)})
                
                if response.ok:
                    print("-----------------------Successfully extracted info in json form-----------------------")
                else:
                    print("-----------------------Error while extracting info from playlist-----------------------")
                    print("Exiting program")
                    sys.exit()
                
                response_json = response.json()
                
                for feat_list in response_json["audio_features"]:
                    dict = {"danceability": feat_list["danceability"],
                            "energy": feat_list["energy"],
                            "key": feat_list["key"],
                            "loudness": feat_list["loudness"],
                            "mode": feat_list["mode"],
                            "speechiness": feat_list["speechiness"],
                            "acousticness": feat_list["acousticness"],
                            "instrumentalness": feat_list["instrumentalness"],
                            "liveness": feat_list["liveness"],
                            "valence": feat_list["valence"],
                            "tempo": feat_list["tempo"],
                            "type": feat_list["type"],
                            "time_signature": feat_list["time_signature"],
                            "id": feat_list["id"],
                            "uri": feat_list["uri"]}
                    
                    info_list.append(dict)
        
        self.df = pd.DataFrame(info_list)

        #print(df)
        


    def call_refresh(self):
        print("Refreshing token...")
        refreshCaller = Refresh()
        
        self.spotify_token = refreshCaller.refresh()

        # I think remove this call and and call separetly from main



gym = LoadPlaylist()
gym.call_refresh()
gym.info_extraction(iter=2)
gym.df.to_csv('gym.csv',index=False)

spark = LoadPlaylist(spark_playlist_id, gym.spotify_token)
spark.info_extraction()
spark.df.to_csv('spark.csv',index=False)

hindi = LoadPlaylist(hindi_playlist_id, gym.spotify_token)
hindi.info_extraction()
hindi.df.to_csv('hindi.csv',index=False)

sleep = LoadPlaylist(sleep_playlist_id, gym.spotify_token)
sleep.info_extraction()
sleep.df.to_csv('sleep.csv',index=False)

night = LoadPlaylist(night_playlist_id, gym.spotify_token)
night.info_extraction()
night.df.to_csv('night.csv',index=False)

#print(a.df)

spot_tok = gym.spotify_token







