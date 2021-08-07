#Steam profile pictures use hashing for image name/url
import requests
import urllib.request
import json
import math
import time
import os

#Path to working directory
####################filePath = ''
## WARNING: WILL NOT WORK, WORKING DIR IS FILE LOCATION

#Depth to search. 1: Friends of Seed, 2: Friends of friends, 3: Friends of friends of friends (recommend no number higher than 3)
searchDepth = 2

#Hard-limit number of API requests in case searchDepth is entered incorrectly
queryLimit = 44

class SteamCollage:
    def __init__(self, searchDepth, queryLimit):
        
        self.filePath = os.path.dirname(os.path.realpath(__file__))
        self.searchDepth = searchDepth
        self.queryLimit = queryLimit
        self.fileName = ''

        self.downloadPath = os.path.join(self.filePath, "images")
        if not os.path.exists(self.downloadPath):
            os.mkdir(self.downloadPath)

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

        #print(type(dataUnsorted))

        dataSorted = sorted(dataUnsorted)
        #print(type(dataSorted))

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
            return urllib.request.urlopen('https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='+self.apiKey+'&steamids='+steamID).read().decode('utf8')

        def imgDL(url):
            r = requests.get(url, allow_redirects=True)
            with open(self.downloadPath + '\\' + steamID_ + '.jpg', 'wb') as file:
                file.write(r.content)

        with open(self.fileName) as file:
            fileContent = json.load(file)

        print(len(fileContent))

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

    #def ImageCombine():
        #from PIL import Image
        #import glob
        #import math

        #filePath = '\\Desktop\\'
        #downloadPath = '\\Desktop\\steamIcons\\'

        #def imageLine():
        #    x = glob.glob(downloadPath+'*.jpg')
        #    print(len(x))
        #    a = (int(math.floor(len(x)/120)))
        #    b = (int(len(x)%120))
        #    for n in range(a):
        #        x_offset = 0
        #        images = []
        #        lineImage = Image.new('RGB', (120*32, 32))
        #        for i in range(120):
        #            images.append(Image.open(x.pop(0)))
        #        for j in images:
        #            lineImage.paste(j, (x_offset,0))
        #            x_offset += j.size[0]
        #        lineImage.save(filePath+'inc\\_'+str(n)+'_incremental.jpg')
        #    x_offset = 0
        #    images = []
        #    lineImage = Image.new('RGB', (b*32, 32))
        #    for i in range(b):
        #        images.append(Image.open(x.pop(0)))
        #        print(len(x))
        #    for j in images:
        #        lineImage.paste(j, (x_offset,0))
        #        x_offset += j.size[0]
        #        print(len(x))
        #    lineImage.save(filePath+'inc\\_'+str(a)+'_incremental.jpg')

        ##def lineStack():
        ##    y = glob.glob(filePath+'inc\\'+'*_incremental.jpg')
        ##    print(y)
        ##    stackImage = Image.new('RGB', (120*32, len(y)*32))
        ##    images = []
        ##    y_offset = 0
        ##    for i in range(len(y)):
        ##        images.append(Image.open(y.pop(0)))
        ##        print(len(y))
        ##    for i in images:
        ##        stackImage.paste(i, (0,y_offset))
        ##        y_offset += 32
        ##    stackImage.save(filePath+'inc\\Collage.jpg')

        #def stackStack(number):
        #    y = glob.glob(filePath+'inc\\'+str(number)+'\\'+'*_incremental.jpg')
        #    print(len(y))
        #    stackImage = Image.new('RGB', (120*32, len(y)*32))
        #    images = []
        #    y_offset = 0
        #    for i in range(len(y)):
        #        images.append(Image.open(y.pop(0)))
        #        print(len(y))
        #    for i in images:
        #        stackImage.paste(i, (0,y_offset))
        #        y_offset += 32
        #    stackImage.save(filePath+'inc\\'+str(number)+'.jpg')

        #def collage():
        #    z = glob.glob(filePath+'inc\\'+'*.jpg')
        #    images = [Image.open(i) for i in z]
        #    widths, heights = zip(*(j.size for j in images))
        #    cImage = Image.new('RGB', (max(widths), sum(heights)))
        #    y_offset = 0
        #    count = 0
        #    for n in images:
        #        cImage.paste(n, (0,y_offset))
        #        y_offset += heights[count]
        #        count += 1
        #    cImage.save(filePath+'inc\\Collage.jpg')

        ##imageLine()
        ##for i in range(5):
        ##    stackStack(i)

        #collage()


if __name__ == '__main__':
    SC = SteamCollage(searchDepth, queryLimit)
    SC.Spider()
    SC.ListCombine()
    SC.Sorting()
    SC.UniqueID()
    SC.ImageDL()
