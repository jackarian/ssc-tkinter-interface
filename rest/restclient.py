import requests
import json

from requests import Response


class SscClient:
    def __init__(self, host, plc):
        self.host = host
        self.plc = plc
        self.header = self.getHeader()

    @staticmethod
    def getHeader():
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',

        }
        return headers

    def getResource(self):
        return requests.get(self.host + '/api/resource')

    def getPlc(self):
        return requests.get(self.host + '/api/plc')

    def sendPayload(self, token=None, plc=None):
        response: Response = requests.request("GET", self.host + '/validate/token/'+token, headers=self.header)
        return response


if __name__ == '__main__':
    client = SscClient('http://localhost:8080/ssc', 9900001)
    try:
        response = client.getPlc()
        payload = response.json()
        for resource in payload['result']: print(resource)

    except Exception as e:

        print('Connection error %s' % e)

    # client.sendPayload()
