<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
  <h1 align="center">Spotify Cluster Analysis</h1>
  <h3 align="center">Cluster analysis of <a href="https://drive.google.com/file/d/1_L15Fzhs-vgLeaaeUlwOiCqjZaKxBfqe/view?usp=sharing">Spotify Data</a> sourced from Kaggle (Feb. 2023)</h3>
</body>
    <p> Using Spotify musical characterization including: Energy, Loudness, Tempo, Acousticness, Instrumentalness as well as streaming count statistics aggregated to the artist level we looked for patterns
      amongst artists and their muscial style. K-Means Clustering was employed to group artists based on their average musical characterization. Total Spotify song stream, YouTube views, likes, and comments
      were not used in clustering so as to avoid baising the model with popularity. Once artists were sorted into clusters, their songs were tagged with the artist cluster assignment and aggregation was used 
      to determine descriptive statistics of each cluster.</p>
  <p align="center"><img src="https://github.com/evanjconnolly/Spotify-Cluster-Analysis/blob/main/spot_clust.png?raw=true"></p>
  <p>To better understand the contents of these distinctive clusters the K Means model defined the most streamed artists within each cluster were collected into a table as were the most streamed song from each cluster.</p>
  <p align="center"><img src="https://github.com/evanjconnolly/Spotify-Cluster-Analysis/blob/main/Cluster%20top%20Performers.png?raw=true"></p>
  
</html>
