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

        # Defining the api-endpoint
        url = 'https://api.abuseipdb.com/api/v2/blacklist'

        querystring = {
            'confidenceMinimum':'85'
        }

        headers = {
            'Accept': 'application/json',
            'Key': self.config.ABUSEIPDB_API_KEY
        }

        response = requests.request(method='GET', url=url, headers=headers, params=querystring)
        if(response.status_code==200):
            # update abuseipdb_sample.json
            decodedResponse = json.loads(response.text)
            #clear the content in file
            with open(self.config.JSON_FILE_PATH, "w") as json_file:
                json_file.close()
            #add content to file
            with open(self.config.JSON_FILE_PATH, "w") as json_file:
                json.dump(decodedResponse, json_file, indent=4)
        
        xlsxFileExists = os.path.exists(self.config.XLSX_FILE_PATH)

        if(xlsxFileExists!=True):
            return []

        with open(self.config.JSON_FILE_PATH) as f:
            jsonData = json.load(f)
        
        extractedIps = []

        for data in jsonData['data']:
            extractedIps.append(data['ipAddress'])

        print("Finished Ip Extraction")

        return extractedIps


    def saveAsXlsx(self):

        print("Started saving")

        self.jsonToXlsx.convert()

        print("Finished saving")
        
