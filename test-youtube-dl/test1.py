from ytmusicapi import *
import urllib.request
import eyed3
import os

ytmusic = YTMusic()
# url:str = input("Playlist URL : ")
# savedir:str = input("Directory to save to : ")
# audformat:str = input("Audio format to use : ")

url:str = "https://www.youtube.com/playlist?list=PLeG6U6mYSDogd8J0478lQ461r26bfYg70"
savedir:str = "C:\\Users\\chong\\Music\\Music Tracks\\good vibes (1)"
audformat:str = "mp3"

playlist:dict = ytmusic.get_playlist(playlistId=url[url.find("list=")+5:],limit=None)
tracks:list = playlist["tracks"]
for i in range(len(tracks)):
    curtrack:dict = tracks[i]
    url:str = curtrack["videoId"]
    curtrack:list = ytmusic.search(query=curtrack["title"],filter="songs",limit=2)
    curtrack:dict = curtrack[0] if len(curtrack[0]["title"]) < len(curtrack[1]["title"]) else curtrack[1]
    # extract song information
    title:str = curtrack["title"]
    trackdir:str = savedir + "\\" + title + "." + audformat
    artist:str = curtrack["artists"][0]["name"]        
    thumbnail:str = curtrack["thumbnails"][-1]["url"]
    album:str = curtrack["album"]["name"]
    
    # set thumbnail height/width
    thumbnail = thumbnail[:thumbnail.find("=")] + "=w480-h480-l90-rj"
    img:bytes = urllib.request.urlopen(thumbnail).read()

    # check if it already exists
    if (not os.path.isfile(trackdir)): 
        os.system(f'youtube-dl --extract-audio --audio-format {audformat} --no-part -o "{savedir}\\{title}.%(ext)s" https://www.youtube.com/watch?v={url}')
    
    # call file
    audiofile = eyed3.load(trackdir)
    
    # set version
    audiofile.initTag(version=(2,3,0))

    # set id3 values
    audiofile.tag.artist = artist
    audiofile.tag.album = album
    audiofile.tag.title = title
    audiofile.tag.images.set(3,img,"image/jpeg",u"cover")
    audiofile.tag.save()  