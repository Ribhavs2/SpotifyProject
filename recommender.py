
from playlist_ids import beast_mode_hiphop_playlist_id, most_necessary_playlist_id, get_turnt_playlist_id, new_joints_playlist_id
from refresh import Refresh
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from playlist_ids import gym_playlist_id
import requests
import json

from dataCollect import LoadPlaylist, spot_tok
from analyzing import threshold, training_model

class Recommender:
    def __init__(self, pool_df):
        self.pool_df = pool_df
        self.selected = pd.DataFrame()
        self.spotify_token = spot_tok
        
    def prediction(self):
        print("-------------------------------------------------------------------")
        print("Predicting using model...")
        self.pool_df["Predicted"] = training_model.predict(exog=dict(self.pool_df))
        #print(self.pool_df.head(10))
        self.selected = self.pool_df[self.pool_df['Predicted'] > 0.9999]
        print("No. of songs selected: ", self.selected.shape[0])
        print("Selection rate:", self.selected.shape[0]/self.pool_df.shape[0])

    def add_selected_to_playlist(self):
        print("-------------------------------------------------------------------")
        print("Adding selected songs to playlist...")
        selected_list = self.selected["uri"].tolist()
        str_selected_list = ','.join(selected_list)
        print(str_selected_list)
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(gym_playlist_id, str_selected_list)
        response = requests.post(query,
                                 headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})

        print(response)



        




b = LoadPlaylist(beast_mode_hiphop_playlist_id, spot_tok)
b.info_extraction()


#c = LoadPlaylist(most_necessary_playlist_id, spot_tok)
#c.info_extraction()


d = LoadPlaylist(get_turnt_playlist_id, spot_tok)
d.info_extraction()


#e = LoadPlaylist(new_joints_playlist_id, spot_tok)
#e.info_extraction()

df_new = pd.concat([b.df, d.df], ignore_index=True)
print("Raw shape:", df_new.shape[0])

df_new = df_new.drop_duplicates()
df_new = df_new[df_new["time_signature"] != 1]
df_new = df_new[df_new["key"] != -1]
print("Shape after dropping duplicates:", df_new.shape[0])

rec_obj = Recommender(df_new)
rec_obj.prediction()
rec_obj.add_selected_to_playlist()

# Check threshold values for prediction










        


