import requests
import json
import os
from JsonToXlsx import JsonToXlsx

class IpExtractor:

    def __init__(self, config):
        self.config = config
        self.jsonToXlsx = JsonToXlsx(self.config)

    def extract(self):

        print("Started Ip Extraction")

        url = 'https://api.abuseipdb.com/api/v2/blacklist'

        querystring = {
            'confidenceMinimum':'85',
             'limit':'50'
        }

        headers = {
            'Accept': 'application/json',
            'Key': self.config.ABUSEIPDB_API_KEY
        }

        response = requests.request(method='GET', url=url, headers=headers, params=querystring)
        
        if(response.status_code==200):

            decodedResponse = json.loads(response.text)
            #clear the content in file
            with open(self.config.JSON_FILE_PATH, "w") as json_file:
                json_file.close()
            #add content to file
            with open(self.config.JSON_FILE_PATH, "w") as json_file:
                json.dump(decodedResponse, json_file, indent=4)
        
        jsonFileExists = os.path.exists(self.config.JSON_FILE_PATH)

        if(jsonFileExists!=True):
            return []

        with open(self.config.JSON_FILE_PATH) as f:
            jsonData = json.load(f)
        
        extractedIps = []

        for data in jsonData['data']:
            extractedIps.append(data['ipAddress'])

        print("Finished Ip Extraction")

        return extractedIps


    def saveAsXlsx(self):

        print("Started saving in xlsx")

        self.jsonToXlsx.convert()

        
