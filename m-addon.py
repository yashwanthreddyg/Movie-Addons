# -*- coding: utf-8 -*-
import os,time,urllib,json,collections
from utils import *
from urllib import FancyURLopener
from guessit import guessit
import urllib
import urllib2
import argparse

class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11; SubDB/1.0'

def addons(path,recursive = False, poster = False, subtitles = False):
    if not os.path.exists(path):
        return False
    isFile = os.path.isfile(path)
    files = []
    if not isFile:
        files = getAllFileNames(path,recursive)
    elif isMediaFileName(path):
        files.append((os.path.basename(path),path))
    else:
        return False
    finalFiles = []
    for file in files:
        if isMediaFileName(file[0]):
            finalFiles.append(file)
    fileDict = {}
    for f in finalFiles:
        fileDict[f[1]] ={}
        guessed = guessit(f[0])
        fileDict[f[1]]['file_details'] = guessed

    # getting movie details from omdb api and writing to file
    for file in fileDict:
        print "retrieving movie details of "+ file
        movieDetails = getMovieDetails(fileDict[file]["file_details"])
        if movieDetails is None:
            print "couldn't retrieve movie details of " + file
            continue
        else:
            print "successfully retrieved movie details of " + file
        fileDict[file]["movie_details"] = movieDetails
        fileName = file[:file.rfind('.')]+".minfo"
        # saving movie details to a .minfo file
        writeFile = None
        try:
            writeFile = open(fileName ,"w+")
            for item in movieDetails:
                decoded = movieDetails[item].encode('ascii', 'ignore').decode('ascii')
                writeFile.write(item + " : " + decoded + "\n")
        except Exception as ew:
            print "couldn't write movie details of "+file+ " to file"
            print ew
        else:
            print "successfully saved movie details of "+file
        finally:
            if writeFile is not None and not writeFile.closed:
                writeFile.close()
        writeFile.close()

        # download poster and save it to disk if the user want it
        if poster and u"Poster" in movieDetails and movieDetails[u"Poster"] != u"N/A":
            posterURL = movieDetails[u"Poster"]
            print "retrieving \"" + fileDict[file]["file_details"]["title"] + "\" poster"
            posterData = getPosterData(posterURL)
            if posterData is not None:
                print "retrieved poster of \"" + fileDict[file]["file_details"]['title'] + "\""
                posterFile = None
                try:
                    posterFile = open(file[:file.rfind('.')] + ".jpg", "wb+")
                    posterFile.write(posterData.read())
                except Exception as ew:
                    print "could not save poster at "+file[:file.rfind('.')]+".jpg"
                    print ew
                else:
                    print "saved poster at "+ file[:file.rfind('.')]+".jpg"
                finally:
                    if posterFile and not posterFile.closed:
                        posterFile.close()
            else:
                print "couldn't retrieve poster of \"" + fileDict[file]["file_details"]['title'] + "\""

            # download subtitle and save to file if the user wants
            if subtitles:
                fname = file[:file.rfind('.')]
                subtitleFile = None
                try:
                    #get has of the file
                    hash  = get_hash(file)
                    base_url = 'http://api.thesubdb.com/?{0}'
                    user_agent = 'SubDB/1.0'
                    params = {'action': 'download', 'language': 'en', 'hash': hash}
                    url = base_url.format(urllib.urlencode(params))
                    req = urllib2.Request(url)
                    req.add_header('User-Agent', user_agent)
                    subData = urllib2.urlopen(req)
                    subtitleFile = open(fname + ".srt", "wb+")
                    subtitleFile.write(subData.read())
                except Exception as e:
                    print "couln't download subtilte of " + file
                else:
                    print "subtitle of "+file+" downloaded"
                finally:
                    if subtitleFile is not None and not subtitleFile.closed:
                        subtitleFile.close()

    return True

def getMovieDetails(fileDetails):
    try:
        if "title" in fileDetails:
            url = "http://www.omdbapi.com/?" + "t=" + fileDetails['title'] + "&tomatoes=true&plot=full"
            print "retrieving \""+ fileDetails["title"] + "\" details"
            response = urllib.urlopen(url).read()
            print "retrieved details of \""+ fileDetails['title'] + "\""
            jsonresponse = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(response)
            return jsonresponse
    except Exception as e:
        print "check connectivity"
        print e
    return None

def getPosterData(posterURL):
    try:
        return urllib.urlopen(posterURL)
    except Exception as e:
        print "error getting "+posterURL
        print e
    return None

if __name__ == "__main__":
    print "Hello World"
    rec = False
    pos = False
    sub = False
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path of the directory or file")
    parser.add_argument("-r", help="finds all files in the folder recursively", action="store_true")
    parser.add_argument("-s", help="download subtitles for files", action="store_true")
    parser.add_argument("-p", help="download posters for files", action="store_true")
    args = parser.parse_args()
    if args.p:
        pos = True
    if args.s:
        sub = True
    if args.r:
        rec = True

    folderPath = args.path.decode("utf-8")
    asciiFolderPath = folderPath.encode('ascii','ignore')
    addons(folderPath,rec,pos,sub)