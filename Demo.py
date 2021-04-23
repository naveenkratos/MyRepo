from IpExtractor import IpExtractor
from MongoConnector import MongoConnector
from VtIpChecker import VtIpChecker
from Mailer import Mailer
import sys
import config
from TableCreator import TableCreator

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
        print("Terminated")
        sys.exit()
    
    tableCreator = TableCreator(config,mongo)

    vtIpChecker = VtIpChecker(config,mongo,tableCreator)
    vtIpChecker.StorebulkIpData(extractedIps)

    htmlTableData = tableCreator.getHtmlTableData()

    mailer = Mailer(config)
    mailer.triggerMail(htmlTableData)

else:

    print("Cant Extract Ips")
