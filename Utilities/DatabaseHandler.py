import os
import pymongo

z1 = os.environ.get('CON2')


class DatabaseHandler():
    def __init__(self):
        self.client = pymongo.MongoClient(os.environ.get('CON0'))
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
