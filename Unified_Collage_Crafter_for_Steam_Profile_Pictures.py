import urllib.request
import json
import time

#Path to working directory
filePath = ''

#Depth to search. 1: Friends of Seed, 2: Friends of friends, 3: Friends of friends of friends (recommend no number higher than 3)
searchDepth = 1

#Hard-limit number of API requests in case searchDepth is entered incorrectly
queryLimit = 3

#Your steam API key here
with open(filePath+'api.txt', 'r') as file: apiKey = file.read()
#apiKey = ''

#SteamID for first account to seed search
with open(filePath+'seed.txt','r') as file: SteamID = file.read()
#seedID = ''



class SteamCollage:
    def __init__(self, apiKey, filePath, seedID, searchDepth, queryLimit):
        self.apiKey = apiKey
        self.filePath = filePath
        self.seedID = seedID
        self.searchDepth = searchDepth
        self.queryLimit = queryLimit
        self.fileName = ''

    def APIpull(self, steamID):
        return urllib.request.urlopen('https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key='+apiKey+'&steamid='+steamID).read().decode('utf8')

    def Spider(self, seed=seedID, depth=searchDepth):
        self.fileName = (filePath+r'FriendsList_Depth_'+str(depth)+r'.txt')
        print(self.fileName)

        holdA = [seed]
        holdB = []
        count = 0

        for i in range(depth):
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



    #def ImageDL():
        #filePath = ''
        #fileName = ''

        #dataOld = ""
        #dataNew = ''

        #with open(filePath + fileName, 'r') as file:
        #    dataOld = file.read()

        #dataNew = dataOld.replace("'", '"')

        #with open(filePath + 'FIX_' + fileName, 'w') as file:
        #    file.write(dataNew)

    #def ImageCombine():
        #import urllib.request
        #import requests
        #import json
        #import math

        #filePath = '\\Desktop\\'
        #fileName = 'UNIQUE_SORTED_FIX_FriendsDepth2.json'
        #downloadPath = '\\Desktop\\steamIcons\\'
        #API = ''
        #massive = 100

        #fileContent = []
        #steamIDs = ''

        #history = ["https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/fe/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb.jpg", ""]

        #def apiPull(steamID):
        #    return urllib.request.urlopen('https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='+API+'&steamids='+steamID).read().decode('utf8')

        #def imgDL(url):
        #    r = requests.get(url, allow_redirects=True)
        #    with open(downloadPath + steamID_ + '.jpg', 'wb') as file:
        #        file.write(r.content)

        #with open(filePath + fileName) as file:
        #    fileContent = json.load(file)

        #print(len(fileContent))

        #for i in range(int(math.floor(len(fileContent)/massive))):
        #    if len(fileContent)%massive != 0:
        #        for i in range(len(fileContent)%massive):
        #            steamIDs += (str(fileContent.pop(0)) + '+')
        #        steamIDs = steamIDs[0:-1]
        #        page = apiPull(steamIDs)
        #        pull = json.loads(page)
        #        for i in (pull['response']['players']):
        #            steamID_ = i['steamid']
        #            if i['avatar'] not in history:
        #                imgDL(i['avatar'])
        #                history.append(i['avatar'])
        #    steamIDs = ''
        #    for i in range(massive):
        #        steamIDs += (str(fileContent.pop(0)) + '+')
    
        #    steamIDs = steamIDs[0:-1]
        #    page = apiPull(steamIDs)
        #    pull = json.loads(page)
        #    for i in (pull['response']['players']):
        #        steamID_ = i['steamid']
        #        if i['avatar'] not in history:
        #            imgDL(i['avatar'])
        #            history.append(i['avatar'])



if __name__ == '__main__':
    SC = SteamCollage(apiKey, filePath, seedID, searchDepth, queryLimit)
    SC.Spider()
#    SC.ListCombine()
#    SC.Sorting()
#    SC.UniqueID()