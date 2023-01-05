import ytmusicapi
from urllib.request import urlopen
import eyed3
from os import system, startfile
from os.path import isfile

ytmusic = ytmusicapi.YTMusic()

# savedir = input("Directory Name : ")
savedir:str = "C:\\Users\\chong\\Music\\Music Tracks\\good vibes (1)"

# audformat:str = input("Audio format to use : "
audformat = "mp3"

# url:str = input("Input Youtube Link : ")
url = "https://music.youtube.com/watch?v=tsPrpeaCeh0"
url = url[url.find("=")+1:]
track:dict = [song for song in ytmusic.search(query=ytmusic.get_song(videoId=url)["videoDetails"]["title"]) if "videoId" in song.keys() and song["videoId"] == url][0]

title:str = track["title"]
trackdir:str = savedir + "\\" + title + "." + audformat

if not isfile(trackdir):
    system(f'youtube-dl --extract-audio --audio-format {audformat} --no-part -o "{savedir}\\{track["title"]}.%(ext)s" https://www.youtube.com/watch?v={url}')

trackdir:str = savedir + "\\" + title + "." + audformat
artist:str = track["artists"][0]["name"]        
thumbnail:str = track["thumbnails"][-1]["url"]
album:str = track["album"]["name"]

thumbnail = thumbnail[:thumbnail.find("=")] + "=w480-h480-l90-rj"
img:bytes = urlopen(thumbnail).read()

audiofile = eyed3.load(trackdir)
audiofile.initTag(version=(2,3,0))
audiofile.tag.artist = artist
audiofile.tag.album = album
audiofile.tag.title = title
audiofile.tag.images.set(3,img,"image/jpeg",u"cover")
audiofile.tag.save()  

startfile(trackdir)