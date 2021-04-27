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
        if(response.status_code==200):
            decodedResponse = json.loads(response.text)
            return decodedResponse,response.status_code
        else:
            return {},response.status_code
        
    def MongoStoreIpData(self,ip,ipData):
        processedData = {}
        tableRow = []

        ipDataKeys = list(ipData.keys())

        processedData['ip']=ip
        tableRow.append(processedData['ip'])

        processedData['country'] = ipData['country'] if 'country' in ipDataKeys else 'nil'
        tableRow.append(processedData['country'])

        processedData['as_owner'] = ipData['as_owner'] if 'as_owner' in ipDataKeys else 'nil'
        tableRow.append(processedData['as_owner'])

        

        processedData['detected_urls'] = ipData['detected_urls'] if 'detected_urls'in ipDataKeys else []
        tableRow.append(",".join([json.dumps(processedData['detected_urls'][0])]) if len(processedData['detected_urls'])>0 else "nil")
        
        processedData['undetected_urls'] = ipData['undetected_urls'] if 'undetected_urls'in ipDataKeys else []
        tableRow.append(",".join([json.dumps(processedData['undetected_urls'][0])]) if len(processedData['undetected_urls'])>0 else "nil")
        
        processedData['detected_downloaded_samples'] = ipData['detected_downloaded_samples'] if 'detected_downloaded_samples'in ipDataKeys else []
        tableRow.append(",".join([json.dumps(processedData['detected_downloaded_samples'][0])]) if len(processedData['detected_downloaded_samples'])>0 else "nil")
        
        processedData['undetected_downloaded_samples'] = ipData['undetected_downloaded_samples'] if 'undetected_downloaded_samples'in ipDataKeys else []
        tableRow.append(",".join([json.dumps(processedData['undetected_downloaded_samples'][0])]) if len(processedData['undetected_downloaded_samples'])>0 else "nil")
        
        docPresent = True if len(self.mongo.findOne({'ip':ip})) > 0 else False
        self.mongo.updateOne({'ip':ip},processedData) if docPresent else self.mongo.insertOne(processedData)

        # Multi Data insert

        # self.tableCreator.insertRow([
        #     processedData['ip'],
        #     processedData['country'],
        #     processedData['as_owner'],
        #     "[ "+",".join([json.dumps(item) for item in processedData['detected_urls']])+" ]",
        #     "[ "+",".join([json.dumps(item) for item in processedData['undetected_urls']])+" ]",
        #     "[ "+",".join([json.dumps(item) for item in processedData['detected_downloaded_samples']])+" ]",
        #     "[ "+",".join([json.dumps(item) for item in processedData['undetected_downloaded_samples']])+" ]"
        # ])

        

        self.tableCreator.insertRow(tableRow)

    def StorebulkIpData(self,ips):

        print("started Processing IPs in VirusTotal")
        print("Processing IPs...")

        startTime = time.time()

        for index,ip in enumerate(ips):
            requestStartTime = time.time()

            ipData,statusCode = self.getIpData(ip)

            waitStartTime = time.time()
            while statusCode != 200:

                ipData,statusCode = self.getIpData(ip)
                waitTime = time.time() - waitStartTime
                if(waitTime > 80):
                    print("VT daily Request Limit reached")
                    break 

            self.MongoStoreIpData(ip,ipData)
            
            mongoStoreEndTime = time.time()
            timeTaken = mongoStoreEndTime - requestStartTime
            # if(index+1%self.VIRUSTOTAL_TOTAL_REQ_PER_MIN==0)
            # if(index+1>=3):
            #     break
            # time.sleep(40-timeTaken/self.config.VIRUSTOTAL_TOTAL_REQ_PER_MIN)

        stopTime = time.time()

        self.bulKIpStoreTimeTaken = stopTime-startTime
        print("Finished Processing IPs in VirusTotal")
        print('Time Taken - ',self.bulKIpStoreTimeTaken)

