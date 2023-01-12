import json, requests
from exception import HTTPError, ConnError

class Req:
    def __init__(self):
        self._ipAddr = 'localhost'
        self._head = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
        self._user = 'http://XXXXXXXXXXXX@'
        self._port = 2501

    def setIP(self, ip):
        self._ipAddr = ip
    
    def getIP(self):
        return self._ipAddr

    def get(self, path, params):
        url = self._user + self._ipAddr + ':' + str(self._port) + path
        try:
            response = requests.get(url=url, params=params)
            response.raise_for_status()
            return json.loads(response.text)
        except requests.exceptions.HTTPError:
            raise HTTPError('HTTP error')   
        except requests.exceptions.RequestException:
            raise ConnError('Wrong IP')

    def post(self, path, data):
        url = self._user + self._ipAddr + ':' + str(self._port) + path
        dat = 'json=' + json.dumps(data)
        try:
            response = requests.post(url=url, headers=self._head, data=dat)
            response.raise_for_status()
            return json.loads(response.text)
        except requests.exceptions.HTTPError:
            raise HTTPError('HTTP error')   
        except requests.exceptions.RequestException:
            raise ConnError('Wrong IP')
            