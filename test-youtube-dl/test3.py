import eyed3
from os import listdir, rename
from os.path import isfile, join

dir:str = "C:\\Users\\chong\\Music\\Music Tracks\\good vibes (1)"

files:list = [f for f in listdir(dir) if isfile(join(dir, f))]

for i in range(len(files)):
    file:eyed3.AudioFile = eyed3.load(dir+"\\"+files[i])
    if files[i][files[i].rfind("\\"):files[i].rfind(".mp3")] != file.tag.title:
        rename(str(file),dir+"\\"+file.tag.title+".mp3")