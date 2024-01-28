import requests
import os
import urllib.request
from zipfile import ZipFile

DOWNLOAD_FOLDER_PATH = 'C:/Users/joeik/OneDrive/Documents/Code Repos/LINE-Stamp-Downloader/Downloaded_Images'
# LINE_STAMP_STORE_URL = 'https://stickershop.line-scdn.net/sticonshop/v1/sticon/640fe3e67e1f2c21dbd02b15/iPhone/001_animation.png?v=1' # Jersey-chan emoji set URL example
LINE_STAMP_STORE_URL = 'https://store.line.me/stickershop/product/24573349/en' # Regular Animated Sticker set URL example
APNG2GIF_EXE_PATH = '"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"' # Executeable needs to be put in double quotes to be run by os.system()
GIF_FOLDER_PATH = 'C:/Users/joeik/OneDrive/Documents/Code Repos/LINE-Stamp-Downloader/GIF_Images'
LINE_STAMP_FILE_EXTENSION = '.png' # All LINE Stamps I know of are in APNG (.png) format
EMOJI_SET_NAME = 'Jersey-chan-emoji-6'

def clearFolders():
    pngFilesList = os.listdir(DOWNLOAD_FOLDER_PATH)
    for imageName in pngFilesList:
        os.remove(DOWNLOAD_FOLDER_PATH + imageName)

    gifFilesList = os.listdir(GIF_FOLDER_PATH)
    for gifName in gifFilesList:
        os.remove(GIF_FOLDER_PATH + gifName)

def downloadAnimatedStickerSet():
    # Create download URL, AKA http://dl.stickershop.line.naver.jp/products/0/0/1/3333/iphone/stickers@2x.zip but replace 3333 with the LINE Sticker store ID of the set
    # that you want. Template URL comes from here: https://ldjb.jp/full-resolution-line-sticker-images 
    stickerURLArray1 = LINE_STAMP_STORE_URL.split('product/')
    stickerURLIDArray = stickerURLArray1[1].split('/')
    stickerURLID = stickerURLIDArray[0]

    requestURL = 'http://dl.stickershop.line.naver.jp/products/0/0/1/' + stickerURLID + '/iphone/stickers@2x.zip'
    urllib.request.urlretrieve(requestURL, DOWNLOAD_FOLDER_PATH + '/' + 'animatedStickerSet.zip')

    with ZipFile(DOWNLOAD_FOLDER_PATH + '/animatedStickerSet.zip', 'r') as zip_ref:
        zip_ref.extractall(DOWNLOAD_FOLDER_PATH)

    # Delete unnecessary extra files
    if os.path.exists(DOWNLOAD_FOLDER_PATH + '/productInfo.meta'):
        os.remove(DOWNLOAD_FOLDER_PATH + '/productInfo.meta')

    if os.path.exists(DOWNLOAD_FOLDER_PATH + '/animatedStickerSet.zip'):
        os.remove(DOWNLOAD_FOLDER_PATH + '/animatedStickerSet.zip')

    if os.path.exists(DOWNLOAD_FOLDER_PATH + '/tab_off@2x.png'):
        os.remove(DOWNLOAD_FOLDER_PATH + '/tab_off@2x.png')

    if os.path.exists(DOWNLOAD_FOLDER_PATH + '/tab_on@2x.png'):
        os.remove(DOWNLOAD_FOLDER_PATH + '/tab_on@2x.png')
    
    # Auto delete all _key files
    imageFileNameList = os.listdir(DOWNLOAD_FOLDER_PATH)
    for imageName in imageFileNameList:
        if '_key' in imageName:
            os.remove(DOWNLOAD_FOLDER_PATH + '/' + imageName)

def convertPNGstoGIFs():
    imageFileNameList = os.listdir(DOWNLOAD_FOLDER_PATH)
    for imageName in imageFileNameList:
        windowsCommandString = APNG2GIF_EXE_PATH + ' ' + DOWNLOAD_FOLDER_PATH + '/' + imageName + ' ' + GIF_FOLDER_PATH + '/' + imageName[:-4] + '.gif'
        print(windowsCommandString)
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
        completeFilePath = os.path.join(DOWNLOAD_FOLDER_PATH, EMOJI_SET_NAME + str(i + 1)  + LINE_STAMP_FILE_EXTENSION) # use os.path.join to add path of specific folder to save image to.  
        with open(completeFilePath, 'wb') as handler:
            handler.write(img_data)



def main():
    #downloadEmojiSet()
    #convertPNGstoGIFs()
    downloadAnimatedStickerSet()
    #convertPNGstoGIFs()
    #clearFolders()


if __name__ == "__main__":
    main()
