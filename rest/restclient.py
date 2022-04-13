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

    def sendPayload(self, token=None):

        payload: str = json.dumps({
            "MID": 1,
            "UID": self.plc,
            "MV": "1",
            "ST": 1,
            "FIFO": [
                {
                    "Date": "2021-01-31",
                    "Value": {
                        "ip_address": "10.10.0.156",
                        "timeStamp": " ",
                        "token": ""+token+""
                    }
                }
            ]
        })

        response: Response = requests.request("POST", self.host + '/activation', headers=self.header, data=payload)

        return response


if __name__ == '__main__':
    client = SscClient('http://localhost:8080/ssc')
    try:
        response = client.getPlc()
        payload = response.json()
        for resource in payload['result']: print(resource)

    except Exception as e:

        print('Connection error %s' % e)

    # client.sendPayload()
