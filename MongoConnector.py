from pymongo import MongoClient

class MongoConnector:

    def __init__(self,config):
        self.config = config
        # self.connect()

    def connect(self):

        print("Connecting to Mongo...")

        #Creating a pymongo client
        self.client = MongoClient(self.config.MONGO_HOST , self.config.MONGO_PORT)

        self.db = self.client[self.config.MONGO_DB]

        #Creating a collection
        self.collection = self.db[self.config.MONGO_COLLECTION]

        print("Mongo Connected")

    def insertOne(self,data):

        self.collection.insert_one(data)
        # print(self.collection.find_one())

    def insertMany(self,dataList):

        self.collection.insert_many(dataList)

