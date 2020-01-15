###########################################################################################
# Bruce Rhoades
#
# Generate a random passphrase from files containing words from which to generate the 
# passphrase
###########################################################################################
import os
import secrets
import zipfile


class XKCDPassword:
    @staticmethod
    def generatePassphraseFromWordFiles():       

        print("Start generation of Passphrase from word files")
        wordList = []

        # Create a connection to the "WordList.zip" file
        wordListFileReference = zipfile.ZipFile("WordList.zip")

        # Exctract all of the files inside of "WordList.zip"
        wordListFileReference.extractall()

        # Create a path to the newly created "WordList" folder
        print("Generating Passphrase Step 1: Extracting WordList.zip")
        wordListFolder = os.path.join("WordList")

        # Use navigate through the text files within the "WordList" folder
        for root,dirs,files in os.walk(wordListFolder):

            # Loop through the files at the current root
            for i, file in enumerate(files):

                # Create the path that points to the current file
                currentFilePath = os.path.join(wordListFolder, file)       

                # Create a connection to this file and read its contents
                fileObj = open(currentFilePath, "r")
                print("Generating Passphrase Step {0}: Reading File of words: {1}".format(i+2, file))
                fileText = fileObj.read()
                fileObj.close()

                # Split the wordsText variable on newlines
                splitWordsText = fileText.split("\n")

                # Loop through each element in the splitWordsText list
                for splitWord in splitWordsText:

                    # Push the word into the completeWordList
                    wordList.append(splitWord)

        passphrase = ""

        print("Generating Passphrase")
        for x in range(0, 4):
            # Select a random word and add it to the passphrase
            passphrase = passphrase + "[" + secrets.choice(wordList).capitalize() + "]"
        
        # Print out the passphrase
        print("Passphrase: " + passphrase)
        print("End of generation of Passphrase from word files")
        
