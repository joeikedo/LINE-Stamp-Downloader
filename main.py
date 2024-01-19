import requests
import os

DOWNLOAD_FOLDER_PATH = 'C:/Users/joeik/OneDrive/Documents/Code Repos/LINE-Stamp-Downloader/Downloaded_Images'
LINE_STAMP_STORE_URL = 'https://stickershop.line-scdn.net/sticonshop/v1/sticon/640fe3e67e1f2c21dbd02b15/iPhone/001_animation.png?v=1'
APNG2GIF_EXE_PATH = '"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"' # Executeable needs to be put in double quotes to be run by os.system()
GIF_FOLDER_PATH = 'C:/Users/joeik/OneDrive/Documents/Code Repos/LINE-Stamp-Downloader/GIF_Images'
LINE_STAMP_FILE_EXTENSION = '.png' # All LINE Stamps I know of are in APNG (.png) format
STAMP_SET_NAME = 'Jersey-chan-emoji-6'

def convertPNGstoGIFs():
    imageFileNameList = os.listdir(DOWNLOAD_FOLDER_PATH)
    for imageName in imageFileNameList:
        windowsCommandString = APNG2GIF_EXE_PATH + ' ' + imageName + ' ' + GIF_FOLDER_PATH + '/' + imageName[:-4] + '.gif'
        #os.system(windowsCommandString)
    

# Helper function for downloadEmojiSet() that sets the url from .../iPhone/001_animation.png... to .../iPhone/002_animation.png... etc, based on input index number.
def adjustEmojiSetURL(inputIndex):
    indexOfPhrase = LINE_STAMP_STORE_URL.find('_animation.png')

    # Prepend number to insert into URL with 0's if necessary. 
    inputIndexFormattedString = str(inputIndex)
    if(inputIndex <= 9):
        inputIndexFormattedString = '00' + str(inputIndex)
    elif(inputIndex < 99):
        inputIndexFormattedString = '0' + str(inputIndex)
    
    returnString = LINE_STAMP_STORE_URL[:indexOfPhrase - 3] + inputIndexFormattedString + LINE_STAMP_STORE_URL[indexOfPhrase:]
    return returnString


# Function to download all (40?) images of a LINE emoji set
def downloadEmojiSet():
    NUMBER_OF_EMOJI_STAMPS = 40 # All the emoji stamp sets I've seen on the LINE store come in packs of 40

    for i in range(NUMBER_OF_EMOJI_STAMPS):
        currentIterationImageURL = adjustEmojiSetURL(i + 1) # Start at 1 not 0
        img_data = requests.get(currentIterationImageURL).content
        completeFilePath = os.path.join(DOWNLOAD_FOLDER_PATH, STAMP_SET_NAME + str(i + 1)  + LINE_STAMP_FILE_EXTENSION) # use os.path.join to add path of specific folder to save image to.  
        with open(completeFilePath, 'wb') as handler:
            handler.write(img_data)



def main():
    #downloadEmojiSet()
    convertPNGstoGIFs()


if __name__ == "__main__":
    main()
