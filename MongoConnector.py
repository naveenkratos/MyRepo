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

    def findOne(self,filter):
        return list(self.collection.find(filter))

    def updateOne(self,filter,data):
        self.collection.update_one(filter,{"$set":data})
        print("updated ip:",filter['ip'])

    def insertOne(self,data):
        print("Inserted ip:",data['ip'])
        self.collection.insert_one(data)
        # print(self.collection.find_one())

    def insertMany(self,dataList):

        self.collection.insert_many(dataList)

