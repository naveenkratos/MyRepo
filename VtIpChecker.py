import time
import json
import requests

class VtIpChecker:

    def __init__(self, config,mongo,tableCreator):
        self.config = config
        self.mongo = mongo
        self.tableCreator = tableCreator

    def _fireRequest(self,ip):
        url = 'https://www.virustotal.com/vtapi/v2/ip-address/report'

        querystring = {
            'apikey':self.config.VIRUSTOTAL_API_KEY,
             'ip':ip
        }

        headers = {
            'Accept': 'application/json'
        }

        response = requests.request(method='GET', url=url, headers=headers, params=querystring)

        return response

    def getIpData(self,ip):

        response = self._fireRequest(ip)
        # print(response.status_code)
        if(response.status_code==200):
            decodedResponse = json.loads(response.text)
            return decodedResponse,response.status_code
        else:
            return {},response.status_code
        
    def MongoStoreIpData(self,ip,ipData):
        processedData = {}
        processedData['ip']=ip
        processedData['country'] = ipData['country']
        processedData['as_owner'] = ipData['as_owner']
        ipDataKeys = list(ipData.keys())
        processedData['detected_urls'] = ipData['detected_urls'] if 'detected_urls'in ipDataKeys else []
        processedData['undetected_urls'] = ipData['undetected_urls'] if 'undetected_urls'in ipDataKeys else []
        processedData['detected_downloaded_samples'] = ipData['detected_downloaded_samples'] if 'detected_downloaded_samples'in ipDataKeys else []
        processedData['undetected_downloaded_samples'] = ipData['undetected_downloaded_samples'] if 'undetected_downloaded_samples'in ipDataKeys else []
        # self.mongo.insertOne(processedData)
        docPresent = True if len(self.mongo.findOne({'ip':ip})) > 0 else False
        print(docPresent)
        # if docPresent:
        #     self.mongo.updateOne({'ip':ip},processedData)
        # else:
        #     self.mongo.insertOne(processedData)
        self.mongo.updateOne({'ip':ip},processedData) if docPresent else self.mongo.insertOne(processedData)

        self.tableCreator.insertRow([
            processedData['ip'],
            processedData['country'],
            processedData['as_owner'],
            "[ "+",".join([json.dumps(item) for item in processedData['detected_urls']])+" ]",
            "[ "+",".join([json.dumps(item) for item in processedData['undetected_urls']])+" ]",
            "[ "+",".join([json.dumps(item) for item in processedData['detected_downloaded_samples']])+" ]",
            "[ "+",".join([json.dumps(item) for item in processedData['undetected_downloaded_samples']])+" ]"
        ])

    def StorebulkIpData(self,ips):
        print("started Processing IPs in VirusTotal")
        print("Processing IPs...")
        startTime = time.time()

        for index,ip in enumerate(ips):
            # print(ip)
            requestStartTime = time.time()
            ipData,statusCode = self.getIpData(ip)
            while statusCode != 200:
                ipData,statusCode = self.getIpData(ip)
            self.MongoStoreIpData(ip,ipData)
            mongoStoreEndTime = time.time()
            timeTaken = mongoStoreEndTime - requestStartTime
            # print(timeTaken)
            # if(index+1%self.VIRUSTOTAL_TOTAL_REQ_PER_MIN==0)
            # if(index+1>=3):
            #     break
            # time.sleep(40-timeTaken/self.config.VIRUSTOTAL_TOTAL_REQ_PER_MIN)

        stopTime = time.time()

        self.bulKIpStoreTimeTaken = stopTime-startTime
        print("Finished Processing IPs in VirusTotal")
        print('Time Taken - ',self.bulKIpStoreTimeTaken)

        


