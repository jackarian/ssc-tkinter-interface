import requests
import json


class SscClient:
    def __init__(self, host):
        self.host = host
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
        payload: str = json.dumps({
            "MID": 1,
            "UID": 12321277,
            "MV": "1",
            "ST": 1,
            "FIFO": [
                {
                    "Date": "2021-01-31",
                    "Value": {
                        "ip_address": "10.10.0.156",
                        "timeStamp": " ",
                        "token": "5d77da6bb0fd477a991fcd7ea9ba06436969168536505048"
                    }
                }
            ]
        })

        response = requests.request("POST", self.host + '/activation', headers=self.header, data=payload)
        return response


if __name__ == '__main__':
    client = SscClient('http://localhost:8080/ssc')
    response = client.getPlc()
    payload = response.json()
    for resource in payload['result']: print(resource)
    client.sendPayload()
