#!flask/bin/python
from werkzeug.exceptions import BadRequest
from flask import Flask, request, jsonify, make_response
from dev_data import dev_data, bts_config
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return make_response("Welcome to gPower!")

#Post Device Data	
@app.route('/bts_dls/device_data', methods=['POST'])
def postDeviceData():
	json_data = request.json
	if not 'time' in json_data.keys() or not 'imsi' in json_data.keys() or not 'pos_x' in json_data.keys() or not 'pos_y' in json_data.keys() or not 'rssi' in json_data.keys():
		raise BadRequest('Bad Request: Data incomplete.')
	try:
		time = int(json_data['time'])
		pos_x=int(json_data['pos_x'])
		pos_y=int(json_data['pos_y'])
		rssi=int(json_data['rssi'])
	except ValueError:
		raise BadRequest('Bad Request: Data should only contain numbers.')
	if(rssi<-100):
		cl_bst = getClosestBTS(pos_x,pos_y)
		json_data['closest_bts']=cl_bst
	dev_data.append(json_data)
	return jsonify({'dev_data': json_data})

def getClosestBTS(pos_x,pos_y):
	for bts in bts_config:
		if(pos_x>int(bts['range_minX']) and pos_x<int(bts['range_maxX']) and pos_y>int(bts['range_minY']) and pos_y<int(bts['range_maxY'])):
			return bts['location']
	return ''		
	
#Get all device data	
@app.route('/device_data/', methods=['GET'])
def getAllDeviceData():
	return jsonify({'dev_data': dev_data})
	
#Get all devices	
@app.route('/device/', methods=['GET'])
def getAllDevices():
	all_imsi = []
	for p_data in dev_data:
		if p_data['imsi'] not in all_imsi:
			all_imsi.append(p_data['imsi'])
	return jsonify({'devices': all_imsi})	

#Get data for a particular device	
@app.route('/device_data/<imsi>', methods=['GET'])
def getDeviceData(imsi='0'):
	filtered_data = [data for data in dev_data if data['imsi'] == imsi]
	return jsonify({'dev_data': filtered_data})	
	
#Get data for a particular device	
@app.route('/device_data/<imsi>/signal_strength', methods=['GET'])
def getDeviceSignalData(imsi='0'):
	weak_zone = []
	fair_zone = []
	good_zone = []
	for data in dev_data:
		if(data['imsi']==imsi):
			if(int(data['rssi'])<=-90):
				weak_zone.append((data['pos_x'],data['pos_y']))
			elif(int(data['rssi'])>-90 and int(data['rssi'])<-70):
				fair_zone.append((data['pos_x'],data['pos_y']))
			elif(int(data['rssi'])>=-70):
				good_zone.append((data['pos_x'],data['pos_y']))
	dict = {"weak zone":weak_zone, "fair zone":fair_zone, "good zone":good_zone}			
	return jsonify({'signal_data': dict})	

#Get data for a particular device	
@app.route('/device_data/<imsi>/signal_strength', methods=['GET'])
def getDeviceDataFrequency(imsi='0'):
	for data in dev_data:
		if(data['imsi']==imsi):
			if(int(data['rssi'])<=-70):
				weak_zone.append((data['pos_x'],data['pos_y']))
			elif(int(data['rssi'])>-70 and int(data['rssi'])<-60):
				fair_zone.append((data['pos_x'],data['pos_y']))
			elif(int(data['rssi'])>=-60):
				good_zone.append((data['pos_x'],data['pos_y']))
	dict = {"weak zone":weak_zone, "fair zone":fair_zone, "good zone":good_zone}			
	return jsonify({'signal_data': dict})	

	
@app.errorhandler(400)
def bad_request(error):
    return make_response(error.get_description(), 400)

@app.errorhandler(500)
def internal_error(error):
    return make_response('error: Its a Server Error.', 500)	
	
if __name__ == '__main__':
	app.run(debug=True)