import os
import pymongo
import urllib.parse

z1 = os.environ.get('CON2')
mdbuser = urllib.parse.quote_plus(os.environ.get('CON0u'))
mdbpass = urllib.parse.quote_plus(os.environ.get('CON0p'))
mdbaddress = os.environ.get('CON0')
mdbTargetDB = os.environ.get('CON0db')


class DatabaseHandler():
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://" + mdbuser + ":" + mdbpass + "@" + mdbaddress + "/?authSource=" + mdbTargetDB + "&authMechanism=SCRAM-SHA-256")
        self.dbHandler = self.client[os.environ.get('CON1')]

    def getAllBadWordsSYNC(self):
        bwList = []
        bwCursor = self.dbHandler[z1].find()
        for entry in bwCursor:
            bwList.append(entry)
        return bwList

    async def getAllBadWords(self):
        bwList = []
        bwCursor = self.dbHandler[z1].find()
        for entry in bwCursor:
            bwList.append(entry)
        return bwList

    async def addBadWord(self, word: str):
        try:
            query = {"badword": word}
            x = self.dbHandler[z1].insert_one(query)
            return 0
        except:
            print("Exception during addition!")
            return 1

    async def removeBadWord(self, word: str):
        try:
            query = {"badword": word}
            x = self.dbHandler[z1].delete_one(query)
            return 0
        except:
            print("Exception during removal!")
            return 1
