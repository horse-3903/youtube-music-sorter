import ytmusicapi
from song_funcs import *

ytmusic = ytmusicapi.YTMusic()
url = "https://www.youtube.com/playlist?list=PLeG6U6mYSDogd8J0478lQ461r26bfYg70"
path = r"C:/Users/chong/Desktop/Coding/youtube-music-sorter/test-songs/"

# info = get_song_info(video_id=get_video_id(url))
playlist = ytmusic.get_playlist(get_id(url))["tracks"]
start = int(input(f"Start index (0 - {len(playlist)-1}): "))

for index, track in enumerate(playlist):
    if index < start:
        continue
    song_info = get_song_info(res=track)
    download_song(f"https://www.youtube.com/watch?v={song_info['video_id']}", path, title=song_info["title"])
    set_info(path+song_info["title"]+".mp3", song_info)
