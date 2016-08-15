# Movie Addon

### This pyton application lets you easily download additional info, posters and subtitles to all of your video files easily.

####The application can recursively collect all the video files in a folder and it's subfolders
####Additional information about a movie include its title, year, director, ratings (imdb and rotten tomatoes), plot, etc. The info is saved as a '.minfo'(text based) file beside the original video file.

####The application can also download posters as .jpg and subtitles as '.srt'
####Requirements
Python >2.5 <3.0

####Installation:
```
pip install -r requirements.txt
```

####Usage:
```
$python m-addon.py [-h] [-r] [-s] [-p] path

positional arguments:
  path        path of the directory or file

optional arguments:
  -h, --help  show this help message and exit
  -r          finds all files in the folder recursively
  -s          download subtitles for files
  -p          download posters for files
  -d          delete all .minfo files recursively
```

####Example

```
$python m-addon.py -prs .
```

###Notice:
> I haven't tested in on Linux machines but I expect it to work anyway (ty Python).
> In case of any bugs or errors please raise an issue.
