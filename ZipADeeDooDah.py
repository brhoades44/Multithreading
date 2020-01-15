###########################################################################################
# Bruce Rhoades
#
# Unzip a set of musicsheets from a locked zip file
###########################################################################################
 
import threading
import time
import zipfile

class ZipADeeDooDah(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.extractLockedZipFile()
        
    def extractLockedZipFile(self):
        print("Start Extracting MusicSheets.zip")

        # Create a reference to a locked ZIP file
        zipFileReference = zipfile.ZipFile("MusicSheets.zip")
        password = "ComicSans"
        
        zipFileReference.extractall(pwd=password.encode('cp850','replace'))
        print("End Extracting MusicSheets.zip")
 
