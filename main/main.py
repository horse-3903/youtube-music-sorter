import ytmusicapi
import json

ytmusic = ytmusicapi.YTMusic()
url = "https://music.youtube.com/playlist?list=PLeG6U6mYSDogd8J0478lQ461r26bfYg70&si=1gYpgGXQRrvzSJCv"
id = "PLeG6U6mYSDogd8J0478lQ461r26bfYg70"

playlist = ytmusic.get_playlist(id, limit=None)
tracks = playlist["tracks"]

for i, t in enumerate(tracks):
    title = t["title"]
    artist = t["artists"][0]["name"]

    videoID = ytmusic.search(title + " " + artist)
    
    video = ytmusic.get_song(videoID)

    break
