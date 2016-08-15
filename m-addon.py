# -*- coding: utf-8 -*-
import os,time,urllib,json,collections
from utils import *
from guessit import guessit
import urllib2
import argparse


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
        movieDetails = getMovieDetails(fileDict[file]["file_details"])
        if movieDetails is None:
            log("E: FETCH DETAILS: Couldn't retrieve details of "+file,bcolors.FAIL)
        else:
            log("S: FETCH DETAILS: Successfully retrieved details of " + file,bcolors.OKGREEN)
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
                log("E: WRITE DETAILS: Couldn't write details of "+file,bcolors.FAIL)
                print ew
            else:
                log("S: WRITE DETAILS: Successfully wrote details of "+file,bcolors.OKGREEN)
            finally:
                if writeFile is not None and not writeFile.closed:
                    writeFile.close()

        # download poster and save it to disk if the user want it
        if movieDetails is not None and poster and u"Poster" in movieDetails and movieDetails[u"Poster"] != u"N/A":
            posterURL = movieDetails[u"Poster"]
            posterData = getPosterData(posterURL)
            if posterData is not None:
                log("S: FETCH POSTER: Successfully fetched poster of "+file,bcolors.OKGREEN)
                posterFile = None
                try:
                    posterFile = open(file[:file.rfind('.')] + ".jpg", "wb+")
                    posterFile.write(posterData.read())
                except Exception as ew:
                    log("E: WRITE POSTER: Couldn't save poster of "+file,bcolors.FAIL)
                    print ew
                else:
                    log("S: WRITE POSTER: Successfully saved poster of "+file,bcolors.OKGREEN)
                finally:
                    if posterFile and not posterFile.closed:
                        posterFile.close()
            else:
                log("S: FETCH POSTER: Successfully fetched poster of "+file,bcolors.OKGREEN)

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
                log("E: FETCH SUBTITLE: Couldn't fetch subtitle of "+file,bcolors.FAIL)
            else:
                log("S: WRITE SUBTITLE: Successfully saved subtitle of "+file,bcolors.OKGREEN)
            finally:
                if subtitleFile is not None and not subtitleFile.closed:
                    subtitleFile.close()

    return True

def getMovieDetails(fileDetails):
    try:
        if "title" in fileDetails:
            url = "http://www.omdbapi.com/?" + "t=" + fileDetails['title'] + "&tomatoes=true&plot=full"
            response = urllib.urlopen(url).read()
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
    rem = False
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path of the directory or file")
    parser.add_argument("-r", help="finds all files in the folder recursively", action="store_true")
    parser.add_argument("-s", help="download subtitles for files", action="store_true")
    parser.add_argument("-p", help="download posters for files", action="store_true")
    parser.add_argument("-d", help="delete all .minfo files recursively", action="store_true")
    args = parser.parse_args()

    if args.d:
        deleteMInfoFiles(unicode(args.path,'utf-8'))
        print "done"
        exit()
    if args.p:
        pos = True
    if args.s:
        sub = True
    if args.r:
        rec = True

    addons(unicode(args.path,'utf-8'),rec,pos,sub)