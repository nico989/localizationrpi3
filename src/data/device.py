from req import Req
from exception import HTTPError, ConnError
from mathOperation import arithmeticMean, truncate
import time

class Device(Req):
    def __init__(self):
        super().__init__()
        self._paths = ['/devices/views/phy-IEEE802.11/devices.json', '/devices/views/phydot11_accesspoints/devices.json', 
                       '/system/timestamp.json', '/devices/by-mac/', '/devices.json']
        self._fields = {'fields': [ 'kismet.device.base.macaddr',
                                    'kismet.device.base.manuf',
                                    'kismet.device.base.channel',
                                    'kismet.device.base.frequency',
                                    'kismet.device.base.signal/kismet.common.signal.last_signal',
                                    'kismet.device.base.type',
                                    'kismet.device.base.last_time',
                                    'kismet.device.base.signal/kismet.common.signal.max_signal',
                                    'kismet.device.base.signal/kismet.common.signal.min_signal'
                                    ]
                        }
        self._K = 18.4054 #14.1641
        self._A = -46.6820 #-52.3064

    def setIndoor(self):
        self._K = 18.4054
        self._A = -46.6820

    def setOutdoor(self):
        self._K = 0.0
        self._A = 0.0

    def getAll(self):    
        return self.post(self._paths[0], self._fields)
        
    def getAccessPoint(self):
        return self.post(self._paths[1], self._fields)   

    def getDeviceByMAC(self, macAddr):
        return self.post(self._paths[3] + macAddr + self._paths[4], self._fields)

    def getClients(self):
        clients = []
        devices = self.post(self._paths[0], self._fields)
        for device in devices:
            if device[self._fields['fields'][5]]=='Wi-Fi Client':
                clients.append(device)
        return clients

    def getClientsLastTimeSec(self, seconds):
        clients = []
        initialTime = self.get(self._paths[2], None)
        devices = self.post(self._paths[0], self._fields)
        for device in devices:
            if device[self._fields['fields'][5]]=='Wi-Fi Client' and initialTime['kismet.system.timestamp.sec'] - device[self._fields['fields'][6]] < seconds :
                clients.append(device)
        return clients

    def findDevices(self, devices, field, find):
        for device in devices:
            if device[field]==find:
                return device
    
    def filterFields(self, devices, field):
        listDev = []
        for device in devices:
            listDev.append(device[field])
        return listDev
    
    def calcDistanceInstant(self, power):
        distance = pow(10, (self._A-power)/self._K)
        return truncate(distance, 3)

    def calcDistanceAccurateSample(self, macAddr, sample):
        try:
            sampleRSSI = []
            for s in range (sample):
                device = self.getDeviceByMAC(macAddr)
                sampleRSSI.append(device[0]['kismet.common.signal.last_signal'])
            meanPower = arithmeticMean(sampleRSSI)
            return self.calcDistanceInstant(meanPower)
        except HTTPError as http:
            return
        except ConnError as conn:
            return
    
    def calcDistanceAccurateSec(self, macAddr, seconds):
        try:
            initTime = time.time()
            sampleRSSI = []
            while (time.time() - initTime) < seconds:
                device = self.getDeviceByMAC(macAddr)
                sampleRSSI.append(device[0]['kismet.common.signal.last_signal'])
            meanPower = arithmeticMean(sampleRSSI)
            return self.calcDistanceInstant(meanPower)
        except HTTPError as http:
            return
        except ConnError as conn:
            return
    