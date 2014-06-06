#!/usr/bin/python
import wifileds
import time

from flask import Flask
app = Flask(__name__)

IPADDR='192.168.0.17'
PORT=8899

def getBridge():
	return wifileds.limitlessled.connect('192.168.0.17', 8899)

@app.route('/')
def hello_world():
    return 'Light Server'

@app.route('/on')
def all_on():
	bri=getBridge()
	bri.white.all_on()
	del bri
	return hello_world();


@app.route('/off')
def all_off():
	bri=getBridge()
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
def zone(z,level):
	bri=getBridge()
	if level == 0:
		bri.white.zone_off(z)
	else:
		bri.white.zone_on(z)
	del bri
	return hello_world();


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000)

