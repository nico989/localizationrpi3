# Server GPS to run on RPI at boot to have latitude, longitude and altitude from GPS module
# Edit sudo nano /etc/profile at the end with sudo python /home/pi/serverGPS.py & for running the script at boot

import socket
import netifaces
import gps
import math

def main():
    print('Start server')
    port = 5000
    host =  netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
    address = (str(host), port)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(address)
    server.listen(5)
    try:
        while True:
            # print('Waiting connection...')
            gpsd = gps.gps(mode=gps.WATCH_ENABLE)
            result = {'latitude' : 0.0, 'longitude': 0.0, 'altitude': float('nan')}
            client, address = server.accept()
            while result['latitude'] == 0.0 or result['longitude'] == 0.0 or math.isnan(result['altitude']):
                result['latitude'] = gpsd.fix.latitude
                result['longitude'] = gpsd.fix.longitude
                result['altitude'] = gpsd.fix.altitude
                gpsd.next()
            # print('latitude: ' + str(result['latitude']) + ' longitude: ' + str(result['longitude']) + ' altitude: ' + str(result['altitude']))
            client.send(bytes(result))
            client.close()
    except:
        print('\n Server GPS went down, restart RPI')

if __name__ == '__main__':
    main()
