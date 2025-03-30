from pytube import Playlist
from http.client import IncompleteRead

# URL of the YouTube playlist
playlist_url = 'https://www.youtube.com/watch?v=kj0T4aXXxWw&list=PLPeI_PC-QrzgCM33mSRBo8TeEaoUTgsP-&ab_channel=MoviementaProductions'

# Custom output directory
output_directory = '/home/stavros/Downloads/omilos'

# Create a Playlist object
playlist = Playlist(playlist_url)

# Iterate through the videos in the playlist and download them to the custom directory
for video in playlist.videos:
    print(f"Downloading: {video.title}")
    video.streams.get_highest_resolution().download(output_path=output_directory)

print("Download completed.")
