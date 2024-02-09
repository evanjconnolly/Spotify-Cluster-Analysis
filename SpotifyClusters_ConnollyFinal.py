# -*- coding: utf-8 -*-
"""
Created on Wed May 10 15:59:20 2023

@author: evanc
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans


spotify_data=pd.read_csv(r"Spotify_Youtube.csv")

artist_song_count=spotify_data.groupby("Artist")["Track"].agg(cnt="count").reset_index()

#calculating percentage of artists with 10 songs in data set
print((len(artist_song_count[artist_song_count.cnt==10]))/2079)

plt.hist(artist_song_count.cnt)
plt.show()

#filtering artist data to only artists with 10 songs
artist_ten_songs=artist_song_count[artist_song_count.cnt==10]

print(artist_ten_songs.head())

#filtering song data to only those with 10 songs
data_with_ten_songs=spotify_data[spotify_data["Artist"].isin(artist_ten_songs["Artist"])]

#Aggregating song statistics at the artist level
data_10_songs=data_with_ten_songs.groupby("Artist", as_index=False).agg(total_yt_views = ("Views", np.sum),
                                                                        total_yt_likes = ("Likes", np.sum),
                                                                        total_yt_comments = ("Comments", np.sum),
                                                                        total_sp_streams = ("Stream", np.sum),
                                                                        ave_energy = ("Energy", np.mean),
                                                                        ave_loudness = ("Loudness", np.mean),
                                                                        ave_acousticness = ("Acousticness", np.mean),
                                                                        ave_instrumentalness = ("Instrumentalness", np.mean),
                                                                        ave_tempo = ("Tempo", np.mean)
                                                                        )

#Dropping strings and streaming statistics before cluster model so clusters are built on sound, not popularity
data_10_songs_values=data_10_songs.drop(["Artist", "total_yt_views", "total_yt_likes", "total_sp_streams", "total_yt_comments"],axis=1).values

k=4
kmeans=KMeans(n_clusters=k)
kmeans.fit(data_10_songs_values)
labels=kmeans.labels_
centroids=kmeans.cluster_centers_

#Adding cluster labels back to the artist aggregated data
data_10_songs["clust"]=labels

#Dividing artist aggregated data into seperate cluster data frames
clustzero_data=data_10_songs[data_10_songs.clust==0].sort_values("total_sp_streams", ascending=[False]).reset_index(drop=True)
clustone_data=data_10_songs[data_10_songs.clust==1].sort_values("total_sp_streams", ascending=[False]).reset_index(drop=True)
clusttwo_data=data_10_songs[data_10_songs.clust==2].sort_values("total_sp_streams", ascending=[False]).reset_index(drop=True)
clustthree_data=data_10_songs[data_10_songs.clust==3].sort_values("total_sp_streams", ascending=[False]).reset_index(drop=True)

#Pulling top 5 most popular artists from each cluster based on spotify streams
clustzero_top5_streams=clustzero_data["Artist"].head(5)
clustone_top5_streams=clustone_data["Artist"].head(5)
clusttwo_top5_streams=clusttwo_data["Artist"].head(5)
clustthree_top5_streams=clustthree_data["Artist"].head(5)

#creating table of top artists per cluster
clust_top_5=pd.concat([clustzero_top5_streams,clustone_top5_streams,clusttwo_top5_streams, clustthree_top5_streams], axis=1)

clust_top_5=clust_top_5.set_axis(['cluster1', 'cluster2', 'cluster3', 'cluster4'], axis=1, inplace=False)

#calculate average statistics across each cluster
clust_averages=data_10_songs.groupby("clust", as_index=False).agg(ave_yt_views = ("total_yt_views", np.mean),
                                                                                   ave_yt_likes = ("total_yt_likes", np.mean),
                                                                                   ave_sp_streams = ("total_sp_streams", np.mean),
                                                                                   ave_energy = ("ave_energy", np.mean),
                                                                                   ave_loudness = ("ave_loudness", np.mean),
                                                                                   ave_acousticness = ("ave_acousticness", np.mean),
                                                                                   ave_instrumentalness = ("ave_instrumentalness", np.mean),
                                                                                   ave_tempo = ("ave_tempo", np.mean)
                                                                                   )

#Creating a data frame of the maximum and minimum audio statistics for each of the clusters for use identifying individual songs that match each cluster.
clust_max_min=data_10_songs.groupby("clust", as_index=False).agg(max_energy = ("ave_energy", np.max),
                                                                                 min_energy = ("ave_energy", np.min),
                                                                                 max_loudness = ("ave_loudness", np.max),
                                                                                 min_loudness = ("ave_loudness", np.min),
                                                                                 max_tempo = ("ave_tempo", np.max),
                                                                                 min_tempo = ("ave_tempo", np.min)
                                                                                 )

#Filtering the songs dataframe using the max and min statistics for each cluster and selecting songs by the top 5 most popular artists in each cluster.
clust1_songs=data_with_ten_songs[(data_with_ten_songs["Energy"]<0.9781) & (data_with_ten_songs["Energy"]>0.011724)
                                 & (data_with_ten_songs["Loudness"]<-3.9047) & (data_with_ten_songs["Loudness"]>-34.6258)
                                 & (data_with_ten_songs["Tempo"]<110.164) & (data_with_ten_songs["Tempo"]>40.4627) 
                                 & (data_with_ten_songs["Artist"].isin(clustzero_top5_streams))]

clust2_songs=data_with_ten_songs[(data_with_ten_songs["Energy"]<0.9661) & (data_with_ten_songs["Energy"]>0.07297)
                                 & (data_with_ten_songs["Loudness"]<-1.4701) & (data_with_ten_songs["Loudness"]>-28.2588)
                                 & (data_with_ten_songs["Tempo"]<133.04) & (data_with_ten_songs["Tempo"]>119.578) 
                                 & (data_with_ten_songs["Artist"].isin(clustone_top5_streams))]

clust3_songs=data_with_ten_songs[(data_with_ten_songs["Energy"]<0.9705) & (data_with_ten_songs["Energy"]>0.26652)
                                 & (data_with_ten_songs["Loudness"]<-1.7457) & (data_with_ten_songs["Loudness"]>-15.0579)
                                 & (data_with_ten_songs["Tempo"]<165.258) & (data_with_ten_songs["Tempo"]>132.677) 
                                 & (data_with_ten_songs["Artist"].isin(clusttwo_top5_streams))]

clust4_songs=data_with_ten_songs[(data_with_ten_songs["Energy"]<0.975) & (data_with_ten_songs["Energy"]>0.01772)
                                 & (data_with_ten_songs["Loudness"]<-1.9689) & (data_with_ten_songs["Loudness"]>-31.376)
                                 & (data_with_ten_songs["Tempo"]<120.475) & (data_with_ten_songs["Tempo"]>106.388) 
                                 & (data_with_ten_songs["Artist"].isin(clustthree_top5_streams))]


#heatmap of song based data frame
sns.heatmap(spotify_data.corr())
plt.show()

#heatmap of artist aggregated dataframe
sns.heatmap(data_10_songs.corr(), annot=True)
plt.show()

#heatmap of cluster aggregated dataframe
sns.heatmap(clust_averages.corr(), annot=True)
plt.show()

