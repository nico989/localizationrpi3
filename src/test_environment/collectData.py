import time, requests, json

class CollectData:
    def __init__(self, ip, macAddr):
        self._head = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}
        self._url = 'http://XXXXXXXXX@' + ip +':2501/devices/by-mac/' + macAddr + '/devices.json'
        self._field = {'fields': [ 'kismet.device.base.signal/kismet.common.signal.last_signal']}
        self._timeout = 30
    
    def collect(self):
        values = []
        actualTime = time.time()
        while(time.time()-actualTime < self._timeout):
            values.append(self._post()[0]['kismet.common.signal.last_signal'])
        return values
    
    def _post(self):
        dat = 'json=' + json.dumps(self._field)
        response = requests.post(url=self._url, headers=self._head, data=dat)
        return json.loads(response.text)

   
