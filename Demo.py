from IpExtractor import IpExtractor
from MongoConnector import MongoConnector
import config

#Extract Ip from AbuseIPDB
ipExtractor = IpExtractor(config)
extractedIps=ipExtractor.extract()
if(len(extractedIps)>0):
    ipExtractor.saveAsXlsx()

    #MongoConnector
    mongo = MongoConnector(config)
    try:
        mongo.connect()
        # mongo.insertMany([{"sampleKey1":"samplevalue1"},{"sampleKey2":"samplevalue2"}])
    except :
        print("Error in Mongo Connection")

else:

    print("Cant Extract Ips")
