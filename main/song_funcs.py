import requests
import eyed3 
from PIL import Image
import subprocess
import os
import tempfile
import validators
import ytmusicapi
from google_reverse_image_search.google_reverse_search import *

def download_song (url:str, path:str, title:str):
    # check url
    if validators.url(url) and requests.get(url).status_code == 200:
        subprocess.call(["youtube-dl", url, "-x", "--audio-format", "mp3", "--ffmpeg-location", "./ffmpeg.exe", "--hls-prefer-native", "-o", path+f"{title}.%(ext)s"], shell=True)
    else:
        raise ConnectionError(f"{url} is not a valid link")

def set_info (file_path:str, info:dict):
    audiofile = eyed3.load(file_path)
    audiofile.initTag(version=(2,3,0))
    audiofile.tag.title = info["title"]
    audiofile.tag.artist = info["artist"]
    audiofile.tag.album = info["album"]
    img_path = save_temp_thumb(info["thumbnail"])
    audiofile.tag.images.set(3, open(img_path, "rb").read(), "image/jpeg")
    audiofile.tag.save()

def get_song_info (query:str = None, video_id:str = None, thumb_path:str = None, res:dict = {}):
    # keys = ["title", "album", "artist", "video_id", "thumbnail"]
    if video_id:
        return get_song_info(query=get_query(video_id=video_id))
    if res == {}:
        ytmusic = ytmusicapi.YTMusic()
        res = ytmusic.search(query=query, filter="songs")[0]
    
    info = {}
    info["title"] = res["title"]

    info["album"] = res["album"]
    info["album"] = info["album"]["name"] if info["album"] else None

    info["artist"] = res["artists"][0]["name"]

    info["video_id"] = res["videoId"]

    info["thumbnail"] = res["thumbnails"][-1]["url"]
    info["thumbnail"] = info["thumbnail"][:info["thumbnail"].find("=")+1] + "w560-h560-l90-rj"
    return info

def get_id (url:str):
    # https://youtube.com?v=...
    return url[url.find("=")+1:]

def get_query (video_id:str):
    ytmusic = ytmusicapi.YTMusic()
    return ytmusic.get_song(get_id(video_id)).get("videoDetails").get("title")

def save_temp_thumb (url:str = None) -> str:
    response = requests.get(url)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as file:
        file.write(response.content)
        return file.name

# def set_thumbnail (thumb_path:str) -> str:
#     filetypes:list = ['.bmp', '.eps', '.gif', '.ico', '.jpg', '.jpeg', '.msp', '.pcx', '.png', '.ppm', '.tiff', '.webp']
#     if not isfile(thumb_path):
#         raise FileNotFoundError("File does not exist")
#     elif thumb_path[-4:] not in filetypes:
#         raise TypeError("File is not an accepted file type")
    
#     img = Image.open(thumb_path)
#     width:int
#     height:int
#     width, height = img.size
#     if width < 560 or height < 560:
#         new_img = search_with_file(file_path=thumb_path)
#         img = Image.open(new_img)
#         width, height = img.size
#     aspect_ratio:float = width / height

#     if width < height:
#         width = 480
#         height = int(480/aspect_ratio)
#     else:
#         width = int(480*aspect_ratio)
#         height = 480
    
#     img = img.resize((width,height))
    
#     x:int = (width - 480) // 2
#     y:int = (height - 480) // 2

#     img = img.crop((x, y, x + 480, y + 480))
#     file_path = thumb_path[:thumb_path.find(".")] + "-cropped.jpeg"
#     img.save(file_path, format='JPEG')
#     startfile(file_path)
#     return file_path

# def get_song_info (track:dict, thumb_path:str = None) -> dict: 
#     """
#     Gets crucial song information from ytmusicapi search function
#     thumb_path
#     """
#     song_info:dict = {}
#     song_info["title"] = track["title"]

#     if track["album"] != "None":
#         song_info["album"] = track["album"]["name"]
#     else:
#         # assume song is a single
#         song_info["album"] = song_info["title"]

#     song_info["artist"] = track["artists"][0]["name"]
#     song_info["videoId"] = track["videoId"]

#     if not thumb_path:
#         song_info["thumbnail"] = track["thumbnails"][-1]["url"]
#         song_info["thumbnail"] = song_info["thumbnail"][:song_info["thumbnail"].find("=")] + "=w480-h480-l90-rj"
#         song_info["thumbisurl"] = True
#     else:
#         song_info["thumbnail"] = thumb_path
#         song_info["thumbisurl"] = False

#     return song_info

# def assign_id3_info (file_path:str, track_info:str) -> None:
#     """
#     Assigns all track information to file via eyed3
#     """
#     if not isfile(file_path):
#         raise FileNotFoundError("File does not exist")
#     elif file_path[-3:] != ".mp3":
#         raise TypeError("File is not '.mp3' file")
#     audiofile:AudioFile = load(file_path)
#     audiofile.initTag(version=(2,3,0))
#     audiofile.tag.title = track_info["title"]
#     audiofile.tag.artist = track_info["artist"]
#     audiofile.tag.album = track_info["album"]
    
#     # try:


    
# def get_high_res (thumb_path:str):
#     """
#     Google reverse image searches for an image with higher resolution than provided image
#     """
#     # if thumb_path.find("http") != -1:
#     #     search_res:dict = 
#     # else:
#     #     search_res:dict = 

#     # print(search_res)


