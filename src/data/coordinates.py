import math
import numpy
import socket
import ast
from codecs import decode
from mathOperation import degToRad, truncate
from formatPoint import *

class Coordinates:
    def __init__(self):
        self._port = 5000
        self._ip = ''
        self._llh = []
        self._xyz = []
        self._rad = 6378137.0
        self._f = 1.0 / 298.257224
    
    def setIP(self, value):
        self._ip = value
    
    def _clearAll(self):
        self._llh.clear()
        self._xyz.clear()
    
    def _geodeticToECEF(self):
        for llh in self._llh:
            cosLat = numpy.cos(degToRad(llh.lat))
            sinLat = numpy.sin(degToRad(llh.lat))
            cosLon = numpy.cos(degToRad(llh.lon))
            sinLon = numpy.sin(degToRad(llh.lon))
            C = 1.0 / math.sqrt(cosLat * cosLat + (1 - self._f) * (1 - self._f) * sinLat * sinLat)
            S = (1.0 - self._f) * (1.0 - self._f) * C
            x = (self._rad * C + llh.alt) * cosLat * cosLon
            y = (self._rad * C + llh.alt) * cosLat * sinLon
            z = (self._rad * S + llh.alt) * sinLat
            xyz = XYZ(x, y, z)
            self._xyz.append(xyz)

    def _ECEFToENU(self):
        positions = []
        for xyz in self._xyz:
            x = -numpy.sin(degToRad(self._llh[0].lon)) * (xyz.x - self._xyz[0].x) + numpy.cos(degToRad(self._llh[0].lon)) * (xyz.y- self._xyz[0].y)
            y = -numpy.sin(degToRad(self._llh[0].lat))*numpy.cos(degToRad(self._llh[0].lon)) * (xyz.x - self._xyz[0].x) - numpy.sin(degToRad(self._llh[0].lat))*numpy.sin(degToRad(self._llh[0].lon)) * (xyz.y - self._xyz[0].y) + numpy.cos(degToRad(self._llh[0].lat)) * (xyz.z - self._xyz[0].z)
            z = numpy.cos(degToRad(self._llh[0].lat))*numpy.cos(degToRad(self._llh[0].lon)) * (xyz.x - self._xyz[0].x) + numpy.cos(degToRad(self._llh[0].lat))*numpy.sin(degToRad(self._llh[0].lon)) * (xyz.y - self._xyz[0].y) + numpy.sin(degToRad(self._llh[0].lat)) * (xyz.z - self._xyz[0].z)
            pos = XYZ(truncate(x, 3), truncate(y, 3), truncate(z, 3))
            positions.append(pos)
        self._clearAll()
        return positions
    
    def getLLH(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((self._ip, self._port))
        data = ast.literal_eval(decode(server.recv(1024), 'utf-8'))
        llh = LLH(truncate(data['latitude'], 4), truncate(data['longitude'], 4), int(data['altitude']))
        server.close()
        self._llh.append(llh)

    def positions(self):
        self._geodeticToECEF()
        return self._ECEFToENU()  
