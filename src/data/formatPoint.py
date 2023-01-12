class LLH:
    def __init__(self, lat=0.0, lon=0.0, alt=0.0):
        self._lat =  lat
        self._lon = lon
        self._alt = alt
    
    @property
    def lat(self):
        return self._lat
    
    @lat.setter 
    def lat(self, value):
        self._lat = value

    @property
    def lon(self):
        return self._lon
    
    @lon.setter 
    def lon(self, value):
        self._lon = value

    @property
    def alt(self):
        return self._alt
    
    @alt.setter 
    def alt(self, value):
        self._alt = value
    
    def __str__(self):
        coord = 'latitude: ' + str(self._lat) + ' longitude: ' + str(self._lon) + ' altitude: ' + str(self._alt)
        return coord

class XYZ:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self._x = x
        self._y = y
        self._z = z
    
    @property
    def x(self):
        return self._x
    
    @x.setter 
    def x(self, value):
        self._x = value
    
    @property
    def y(self):
        return self._y
    
    @y.setter 
    def y(self, value):
        self._y = value
    
    @property
    def z(self):
        return self._z
    
    @z.setter 
    def z(self, value):
        self._z = value
    
    def __str__(self):
        coord = 'x: ' + str(self._x) + ' y: ' + str(self._y) + ' z: ' + str(self._z)
        return coord
