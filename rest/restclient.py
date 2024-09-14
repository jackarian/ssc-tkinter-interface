import requests
import json

from requests import Response

from opener.opener_interface import OpenerFacade
from opener.opera_lock_operner import OperaLockOpenerFacade


class SscClient:
    def __init__(self, host, plc):
        self.host = host
        self.plc = plc
        self.header = self.getHeader()
        self.opener: OpenerFacade = OperaLockOpenerFacade()

    @staticmethod
    def getHeader():
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer 5f1510234d1d599521bfe86da474e3aacfd058789a61db3d4213d1ba212d99cf63d8167c78d8a679'
        }
        return headers

    def getResource(self):
        return requests.get(self.host + '/api/resource')

    def getPlc(self):
        return requests.get(self.host + '/api/plc')

    def sendPayload(self, token=None, plc=None):
        try:
          response: Response = requests.request("GET", self.host + '/api/activation/token/' + token, headers=self.header)
          return response
        
        except Exception as ex:
            response = Response
            response.status_code = 500
            return response
        
    def validate(self, token=None, plc=None):
        try:          
          response: Response = requests.get(self.host + '/validate/token/' + token)          
          return response
        
        except Exception as ex:                        
            response = Response
            response.status_code = 500
            return response
        
    def apriportaNuki(self):
        try:
          response: Response = requests.request("POST",'https://api.nuki.io/smartlock/18144720508/action/unlock',headers=self.header)
          return response
        
        except Exception as ex:
            response = Response
            response.status_code = 500
            response.reason = ex
            return response
          

    def apriporta(self):
        try:
          self.opener.unlock()
          response = Response
          response.status_code = 200
          return response
        
        except Exception as ex:
            response = Response
            response.status_code = 500
            response.reason = ex
            return response


if __name__ == '__main__':
    client = SscClient('http://service.local:8080/ssc', 9900001)
    ## client.apriporta()
    ##response = client.opener('2a3851a9a3955fb7525564e3e4306b368c32b8131b572361009cba884e945ad7')
    ##print(response)
    ##try:
        ##response = client.getPlc()
        ##payload = response.json()
        ##for resource in payload['result']: print(resource)

    #except Exception as e:
    #    print('Connection error %s' % e)

    # client.sendPayload()
