from ytmusicapi import YTMusic
import pytube
from eyed3 import load
from song_funcs import get_song_info

ytmusic:YTMusic = YTMusic()
# ins:str = input("Insert query or Youtube link : ")
ins:str = "golden hour"
if ins.find("http") != -1:
    ins = ins[ins.find("=")+1:]
    query:str = ytmusic.get_song(videoId=ins)["videoDetails"]["title"]
    track:dict = [song for song in ytmusic.search(query=query, filter="songs") if "videoId" in song.keys() and song["videoId"] == ins][0]
else:
    query:str = ins
    track:dict = [song for song in ytmusic.search(query=query, filter="songs")][0]

