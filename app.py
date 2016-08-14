# -*- coding: utf-8 -*-
import os,time,urllib,json,collections
import shutil
from utils import *
from urllib import FancyURLopener
from guessit import guessit

class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

def addons(folderPath,recursive = False):
    if not os.path.isdir(folderPath):
        return False
    files = getAllFileNames(folderPath,recursive)
    finalFiles = []
    for file in files:
        if isMediaFileName(file[0]):
            finalFiles.append(file)
    fileDict = {}
    for f in finalFiles:
        fileDict[f[1]] ={}
        guessed = guessit(f[0])
        fileDict[f[1]]['file_details'] = guessed
    fileDict = getDetails(fileDict)
    
    print "writing to files"
    for entry in fileDict:
        if not "movie_details" in fileDict[entry]:
            print "no movie details for "+entry
            continue
        if fileDict[entry]["movie_details"]['Response'] == u'False':
            continue

        parentFolderPath = os.path.dirname(entry);
        try:
            name = entry[:entry.rfind('.')]
            writeFile = open(name+".minfo","w+")
            for item in fileDict[entry]["movie_details"]:
                decoded = fileDict[entry]["movie_details"][item].encode('ascii', 'ignore').decode('ascii')
                writeFile.write(item + " : " + decoded + "\n")
            writeFile.close()
            posterData = fileDict[entry].pop("poster_data",None)
            if posterData != None:
                writePoster = open(name+".jpg","wb+");
                writePoster.write(posterData);
                writePoster.close()
            
        except Exception as e:
            print e
        
    print "done with writing to files"
            
    return True

def getDetails(filesDict):
    for file in filesDict:
        fileDetails = filesDict[file]['file_details']
        try:
            if "title" in fileDetails:
                url = "http://www.omdbapi.com/?" + "t=" + fileDetails['title'] + "&tomatoes=true&plot=full"
                print "retrieving \""+ fileDetails["title"] + "\" details"
                response = urllib.urlopen(url).read()
                print "retrieved details of \""+ fileDetails['title'] + "\""
                jsonresponse = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(response)
                filesDict[file]["movie_details"] = jsonresponse
                posterURL = jsonresponse.pop(u"Poster",None)
                if posterURL != None and posterURL!=u"N/A":
                    print "retrieving \""+ fileDetails["title"] + "\" poster"
                    posterData = urllib.urlopen(posterURL)
                    filesDict[file]["poster_data"] = posterData.read()
                    print "retrieved poster of \""+ fileDetails['title']+ "\""
        except Exception as e:
            print "check connectivity"
            print e
    return filesDict

if __name__ == "__main__":
    print "Hello World"
    folderPath = "D:/testFiles"

    folderPath = folderPath.decode("utf-8")
    asciiFolderPath = folderPath.encode('ascii','ignore')
    addons(folderPath,True)