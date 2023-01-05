from os import listdir
from os.path import isfile, join
import eyed3
from urllib.request import urlopen
import ytmusicapi
from PIL import Image
from io import BytesIO

ytmusic = ytmusicapi.YTMusic()

# dir = input("Directory Name : ")
dir:str = "C:\\Users\\chong\\Music\\Music Tracks\\good vibes (1)"

files:list = [f for f in listdir(dir) if isfile(join(dir, f))]

for i in range(len(files)):
    print(i, ":", files[i])
    file:eyed3.AudioFile = eyed3.load(dir+"\\"+files[i])
    print("Title :", file.tag.title)
    print("Artist :", file.tag.artist)
    print("Album :", file.tag.album, "\n")

edit:bool = True
index:int = int(input("Which song no. to start processing : "))

while index < len(files):
    file:eyed3.AudioFile = eyed3.load(dir+"\\"+files[index])
    print(f"\n#{index} - '{file}'")
    print("Title :", file.tag.title)
    print("Artist :", file.tag.artist)
    print("Album :", file.tag.album, "\n")
    if file.tag.images:
        imgdata = BytesIO(file.tag.images[0].image_data)
        img = Image.open(imgdata)
        img.show()
    else:
        print("No thumbnail found")

    edit:bool = {"y":True,"n":False,"":False}[input(f"Edit file No. #{index}? (Y/N) : ").lower()]
    img.close()
    if not edit:
        index += 1
        continue
    
    print("Type '-' if you want to leave it unchanged")
    title:str = input("Title : ")
    file.tag.title = title if title != "" and title != "-" else file.tag.title
    artist:str = input("Artist : ")
    file.tag.artist = artist if artist != "" and artist != "-" else file.tag.artist
    album:str = input("Album : ")
    file.tag.album = album if album != "" and album != "-" else file.tag.album
    
    changethumb:bool = {"y":True,"n":False,"":False}[input("Edit Thumbnail? (Y/N) : ").lower()]

    if changethumb:
        thumbnails:list = [thumb[:thumb.find("=")] + "=w480-h480-l90-rj" for thumb in [song["thumbnails"][-1]["url"] for song in ytmusic.search(query=file.tag.title + file.tag.artist,filter="songs",limit=3)]][:3]
        
        for img in thumbnails:
            img = Image.open(urlopen(img))
            img.show()

        res:str = input("Which thumbnail do you want to use (or ''/'N' to paste url/directory): ")
        if (res.isnumeric()):
            selthumbnail:str = thumbnails[int(res)-1]
            file.tag.images.set(3,urlopen(selthumbnail).read(),"image/jpeg",u"cover")
        else:
            linktothumb:str = input("Paste the URL/Directory of the thumbnail wanted : ")
            if not linktothumb.find("http"):
                selthumbnail:str = linktothumb
                file.tag.images.set(3,urlopen(selthumbnail).read(),"image/jpeg",u"cover")
            elif (isfile(linktothumb)):
                selthumbnail:str = linktothumb
                with open(selthumbnail, "rb") as image_file:
                    file.tag.images.set(3,image_file.read(),"image/jpeg",u"cover")
                

    file.tag.save()
    index += 1

