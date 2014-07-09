#!/usr/bin/python
import wifileds
import time

from flask import Flask
app = Flask(__name__)

PORT=8899
class ColorTypes:
    White=0
    Color=1

zoneMap = [ -1, 0, 0, 0, 0, 1, 1, 1, 1, 2 ]
bridgeIps = { 0:'192.168.0.17', 1:'192.168.0.18', 2:'192.168.0.18'}
zoneTypes = { 0: ColorTypes.White, 1: ColorTypes.White, 2: ColorTypes.Color }

def getBridge(id):  
    return wifileds.limitlessled.connect(bridgeIps[id], 8899)

@app.route('/')
def hello_world():
    return 'Light Server'

@app.route('/on')
def all_on():
    for bridgeId,ip in bridgeIps:
        bri=getBridge(bridgeId)
        bri.white.all_on()
        del bri
    return hello_world();


@app.route('/off')
def all_off():
    bri=getBridge(0)
    bri.white.all_off()
    del bri
    return hello_world();

'''@app.route('/zone/<int:z>')
def zone(z):
    bri=getBridge()
    bri.white.zone_on(z)
    del bri
    return hello_world();
'''


@app.route('/zone/<int:z>/<int:level>')
def zone(z, level):
    id =  zoneMap[z];
    if id == -1:
        allzones(level);
    else:
        bri = getBridge(id)
        zNum = 1 + (z % 4);
        if zoneTypes[id] == ColorTypes.White:
            if level == 0:
                bri.white.zone_off(zNum)
            elif level == 2:
                bri.white.nightlight_zone(zNum)
            else: 
                bri.white.zone_on(zNum)
        elif zoneTypes[id] == ColorTypes.Color:
            if level == 0:
                bri.rgbw.zone_off(zNum)
            elif level == 2:
                bri.rgbw.set_brightness(2,zNum)
            else: 
                bri.rgbw.zone_on(zNum)


        del bri
        return hello_world();

def allzones( level ):
    for id in bridgeIps:
        bri=getBridge(id)
        if level == 0:
            if zoneTypes[id] == ColorTypes.Color:
                bri.rgbw.all_off()
            else:
                bri.white.all_off()
        elif level == 2:
            if zoneTypes[id] == ColorTypes.Color:
                bri.rgbw.all_off()
            else:
                bri.white.nightlight_all()
        else:
            if zoneTypes[id] == ColorTypes.Color:
                bri.rgbw.all_on()
            else:
                bri.white.all_on()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000)

