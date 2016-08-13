import os,time
# from guessit import guessit

def addons(folderPath,recursive = False):
    #print os.path.isdir('./');
    # for d in dirList:
    #     if os.path.isdir(d) == True:
    #         stat = os.stat(d)
    #         created = os.stat(d).st_mtime
    #         asciiTime = time.asctime( time.gmtime( created ) )
    #         print d, "is a dir  (created", asciiTime, ")"
    if not os.path.isdir(folderPath):
        return False
    files = getOnlyFileNames(folderPath,recursive)
    for f in files:
        print f[1]
            
    return True
def getOnlyFileNames(folderPath,recursive = False):
    if recursive:
        return getFileNamesRecursive(folderPath)
    else:
        return getFileNames(folderPath)
def getFileNames(folderPath):
    if not os.path.isdir(folderPath):
        return None
    entries = os.listdir(folderPath)
    files = []
    for entry in entries:
        absPath = os.path.abspath(os.path.join(folderPath,entry))
        if not os.path.isdir(absPath):
            files.append((entry,absPath))
    return files
def getFileNamesRecursive(folderPath):
    if not os.path.isdir(folderPath):
        return None
    files = []
    for entry in os.listdir(folderPath):
        absPath = os.path.abspath(os.path.join(folderPath,entry))
        if os.path.isdir(absPath):
            files.extend(getFileNamesRecursive(absPath))
        else:
             files.append((entry,absPath))
    return files
if __name__ == "__main__":
    print "Hello World"
    addons("D:\\testFiles",True)