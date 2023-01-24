from requests import get
from eyed3 import load, AudioFile
from os.path import isfile
from os import rename, startfile
from PIL import Image

def get_song_info (track:dict, thumb_path:str = None) -> dict: 
    """
    Gets crucial song information from ytmusicapi search function
    thumb_path
    """
    # keys = ["title", "album", "artist", "videoId", "thumbnail", "thumbisurl"]
    song_info:dict = {}
    song_info["title"] = track["title"]

    if track["album"] != "None":
        song_info["album"] = track["album"]["name"]
    else:
        # assume song is a single
        song_info["album"] = song_info["title"]

    song_info["artist"] = track["artists"][0]["name"]
    song_info["videoId"] = track["videoId"]

    if not thumb_path:
        song_info["thumbnail"] = track["thumbnails"][-1]["url"]
        song_info["thumbnail"] = song_info["thumbnail"][:song_info["thumbnail"].find("=")] + "=w480-h480-l90-rj"
        song_info["thumbisurl"] = True
    else:
        song_info["thumbnail"] = thumb_path
        song_info["thumbisurl"] = False

    return song_info

def assign_id3_info (file_path:str, track_info:str) -> None:
    """
    Assigns all track information to file via eyed3
    """
    if not isfile(file_path):
        raise FileNotFoundError("File does not exist")
    elif file_path[-3:] != ".mp3":
        raise TypeError("File is not '.mp3' file")
    audiofile:AudioFile = load(file_path)
    audiofile.initTag(version=(2,3,0))
    audiofile.tag.title = track_info["title"]
    audiofile.tag.artist = track_info["artist"]
    audiofile.tag.album = track_info["album"]
    
    # try:

def set_thumbnail (thumb_path:str) -> str:
    """
    Resizes and crops image to 480x480 size image, saving it as thumb_path-cropped.jpeg
    """
    filetypes:list = ['.bmp', '.eps', '.gif', '.ico', '.jpg', '.jpeg', '.msp', '.pcx', '.png', '.ppm', '.tiff', '.webp']
    if not isfile(thumb_path):
        raise FileNotFoundError("File does not exist")
    elif thumb_path[-4:] not in filetypes:
        raise TypeError("File is not an accepted file type")
    
    img = Image.open(thumb_path)
    width:int
    height:int
    width, height = img.size
    if width < 480 or height < 480:
        new_img = get_high_res()
        img = Image.open(new_img)
        width, height = img.size
    aspect_ratio:float = width / height

    if width < height:
        width = 480
        height = int(480/aspect_ratio)
    else:
        width = int(480*aspect_ratio)
        height = 480
    
    img = img.resize((width,height))
    
    x:int = (width - 480) // 2
    y:int = (height - 480) // 2

    img = img.crop((x, y, x + 480, y + 480))
    file_path = thumb_path[:thumb_path.find(".")] + "-cropped.jpeg"
    img.save(file_path, format='JPEG')
    startfile(file_path)
    return file_path
    
def get_high_res (thumb_path:str):
    """
    Google reverse image searches for an image with higher resolution than provided image
    """
    # if thumb_path.find("http") != -1:
    #     search_res:dict = 
    # else:
    #     search_res:dict = 

    # print(search_res)

get_high_res("https://static.wikia.nocookie.net/princess-connect/images/6/65/Rem-astrum-sprite-normal.png/revision/latest?cb=20190808065750")
