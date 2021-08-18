#improve by staging image downloads per steamID so that only enough images to fill collage resolution downloaded

#improve by allowing pfp image size choices

#add an image integrity verify

#option to organize collage avatars by color

import requests
import urllib.request
import json
import math
import time
import os
import glob
from PIL import Image

#Path to working directory
####################filePath = ''
## WARNING: WILL NOT WORK, WORKING DIR IS FILE LOCATION

#Depth to search. 1: Friends of Seed, 2: Friends of friends, 3: Friends of friends of friends (recommend no number higher than 3)
searchDepth = 1

#Hard-limit number of API requests in case searchDepth is entered incorrectly
queryLimit = 1000

avatarSelect = 1

class SteamCollage:
    def __init__(self, res_x, res_y, searchDepth, queryLimit, avatarSelect):
        self.res_x = int(res_x)
        self.res_y = int(res_y)
        self.filePath = os.path.dirname(os.path.realpath(__file__))
        self.searchDepth = int(searchDepth)
        self.queryLimit = int(queryLimit)
        self.fileName = ''

        if avatarSelect == 1: self.avatar = 'avatar'; self.avatarSize = 32;
        if avatarSelect == 2: self.avatar = 'avatarmedium'; self.avatarSize = 64;

        self.downloadPath = os.path.join(self.filePath, "images")
        if not os.path.exists(self.downloadPath):
            os.mkdir(self.downloadPath)

        self.linePath = os.path.join(self.downloadPath, "lines")
        if not os.path.exists(self.linePath):
            os.mkdir(self.linePath)

        self.stackPath = os.path.join(self.downloadPath, "stack")
        if not os.path.exists(self.stackPath):
            os.mkdir(self.stackPath)

        #Your steam API key
        with open(self.filePath+'\\api.txt', 'r') as file: 
            self.apiKey = file.read()

        #SteamID for first account to seed search
        with open(self.filePath+'\\seed.txt','r') as file: 
            self.seedID = file.read()



    def APIpull(self, steamID):
        return urllib.request.urlopen('https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key='+self.apiKey+'&steamid='+steamID).read().decode('utf8')

    def Spider(self):
        self.fileName = (self.filePath+r'\\FriendsList_Depth_'+str(self.searchDepth)+r'.txt')
        print(self.fileName)

        holdA = [self.seedID]
        holdB = []
        count = 0

        for i in range(self.searchDepth):
            for j in holdA:
                time.sleep(0.1)
                count += 1
                print(count)
                try:
                    page = self.APIpull(j)
                    obj = json.loads(page)
                    for k in (obj['friendslist']['friends']):
                        holdB.append(k['steamid'])
                except Exception as ex:
                    print(ex)
                    pass
                finally:
                    if count >= queryLimit:
                        break
            with open(self.fileName, 'a') as file:
                file.write(json.dumps(holdB))
            holdA = holdB
            holdB = []
    
    def ListCombine(self):
        with open(self.fileName, 'r') as file:
            data = file.read()
        data = data.replace('][', ',')
        with open(self.fileName, 'w') as file:
            file.write(data)

    def Sorting(self):

        dataUnsorted = []

        with open(self.fileName,'r') as file:
            dataUnsorted = json.load(file)

        dataSorted = sorted(dataUnsorted)

        self.fileName = self.fileName+'SORTED_.txt'

        with open(self.fileName, 'w') as file:
            json.dump(dataSorted, file)

    def UniqueID(self):

        data = []
        uniqueData = []

        with open(self.fileName,'r') as file:
            data = json.load(file)

        uniqueData.append(data[0])

        lenData = len(data)

        for i in range(len(data)):
            if uniqueData[-1] != data[0]:
                uniqueData.append(data.pop(0))
            elif uniqueData[-1] == data[0]:
                del data[0]

        lenUData = len(uniqueData)

        print(str(lenData - lenUData) + " duplicates eliminated")

        with open(self.fileName + 'UNIQUE_.txt', 'w') as file:
            json.dump(uniqueData, file)



    def ImageDL(self):

        massive = 100

        fileContent = []
        steamIDs = ''

        history = ["https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/fe/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb.jpg", ""]

        def apiPull2(steamID):
            return urllib.request.urlopen('https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='+self.apiKey+'&steamids='+steamID).read().decode('utf8') #use + between steamID to pull multiple steam IDs

        def imgDL(url):
            r = requests.get(url, allow_redirects=True)
            with open(self.downloadPath + '\\' + steamID_ + '.jpg', 'wb') as file:
                file.write(r.content)

        with open(self.fileName) as file:
            fileContent = json.load(file)

        for i in range(int(math.floor(len(fileContent)/massive))):
            if len(fileContent)%massive != 0:
                for i in range(len(fileContent)%massive):
                    steamIDs += (str(fileContent.pop(0)) + '+')
                steamIDs = steamIDs[0:-1] #???
                page = apiPull2(steamIDs)
                pull = json.loads(page)
                for i in (pull['response']['players']):
                    steamID_ = i['steamid']
                    if i['avatar'] not in history:
                        imgDL(i['avatar'])
                        history.append(i['avatar'])
            steamIDs = ''
            for i in range(massive):
                steamIDs += (str(fileContent.pop(0)) + '+')
    
            steamIDs = steamIDs[0:-1] #???
            page = apiPull2(steamIDs)
            pull = json.loads(page)
            for i in (pull['response']['players']):
                steamID_ = i['steamid']
                if i['avatar'] not in history:
                    imgDL(i['avatar'])
                    history.append(i['avatar'])

    #img size 32x32, 120*32 = 1920*2

    def ImageCombine2(self):

        #create lines
            # glob of images
            # int width of images
            # int length of glob
            # int x/y resolution
            # 

        def imageLine(self):
            imageGlob = glob.glob(os.path.join(self.downloadPath, '*.jpg'))
            imageGlobLen = len(imageGlob)
            if imageGlobLen*(self.avatarSize**2) > self.res_x*self.res_y:
                imageGlob = imageGlob[0:int(self.res_x*self.res_y/(self.avatarSize**2))]
                imageGlobLen = len(imageGlob)
            quotient = (int(math.floor(imageGlobLen/(self.res_x/self.avatarSize))))
            print(quotient)
            
            remainder = (int(imageGlobLen%(self.res_x/self.avatarSize)))
            print(remainder)

            for n in range(quotient):
                x_offset = 0
                images = []
                lineImage = Image.new('RGB', (self.res_x, self.avatarSize))
                for i in range(int(self.res_x/self.avatarSize)):
                    images.append(Image.open(imageGlob.pop(0)))
                for j in images:
                    lineImage.paste(j, (x_offset, 0))
                    x_offset += self.avatarSize
                lineImage.save(os.path.join(self.linePath, (str(n)+'.jpg'))) #self.linePath

            x_offset = 0
            images = []
            lineImage = Image.new('RGB', (remainder*self.avatarSize, self.avatarSize))
            print(remainder)
            print(len(imageGlob))
            if remainder > 0:
                for i in range(remainder):
                    images.append(Image.open(imageGlob.pop(0)))
                for j in images:
                    lineImage.paste(j, (x_offset, 0))
                    x_offset += j.size[0]
                lineImage.save(os.path.join(self.linePath, (str(quotient)+'.jpg')))  ##issue


        def lineStack(self):
            lineGlob = sorted(glob.glob(os.path.join(self.linePath, '*.jpg')), key=len)
            print(lineGlob)
            lineGlobLen = len(lineGlob)
            images = []
            y_offset = 0


            if (lineGlobLen*self.avatarSize) <= self.res_y:
                stackImage = Image.new('RGB', (self.res_x, lineGlobLen*self.avatarSize))
            elif (lineGlobLen*self.avatarSize) > self.res_y:
                lineGlob = lineGlob[0:int((self.res_x/self.avatarSize)*(self.res_y/self.avatarSize))]
                stackImage = Image.new('RGB', (self.res_x, self.res_y))



            for i in range(len(lineGlob)):
                images.append(Image.open(lineGlob.pop(0)))
            for i in images:
                stackImage.paste(i, (0,y_offset))
                y_offset += self.avatarSize
            stackImage.save(os.path.join(self.stackPath, 'stack.jpg'))

        imageLine(self)
        lineStack(self)

        #calculate images per row and column by resolution
        #glob of all images
        #slice glob by number of images needed
        #pop glob and put images in each spot on row
        #glob rows and combine stacks
        #glob stacks and combine

if __name__ == '__main__':
    SC = SteamCollage(40*32, 23*32, searchDepth, queryLimit, avatarSelect)
    #SC.Spider()
    #SC.ListCombine()
    #SC.Sorting()
    #SC.UniqueID()
    #SC.ImageDL()
    SC.ImageCombine2()
