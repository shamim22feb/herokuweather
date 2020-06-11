from flask import Flask, request, make_response
import pyowm
import json, os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
ownkey = '1b37dde14785c8d4061fef7f6c38f8c0'
owm = pyowm.OWM(ownkey)


@app.route('/webhook', methods=['POST','GET'])
@cross_origin()

def webhook():
    # extract city name
    req = request.get_json(silent=False, force=True)
    print(json.dumps(req))
    res = processRequest(req)
    res = json.dumps(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    result = req.get("queryResult")
    parameter = result.get("parameters")
    city = parameter.get("geo-city")
    #mgr = own.weather_manager()
    #observation = mgr.weather_at_place(city)
    observation = owm.weather_at_place(city)
    #w = observation.weather
    w = observation.get_weather()
    wind_res = w.get_wind()
    wind_speed = str(wind_res.get('speed'))

    humidity = str(w.get_humidity())
    #temp_dict_kelvin = w.temperature()  # a dict in Kelvin units (default when no temperature units provided)
    celsius_result = w.get_temperature('celsius')
    temp_min = str(celsius_result.get('temp_min'))
    temp_max = str(celsius_result.get('temp_max'))
    #temp_min = temp_dict_kelvin['temp_min']
    #temp_max = temp_dict_kelvin['temp_max']
    speech = 'Today weather report of '+city+':\n\n'+'Minimum Temperature(in Celsius) : ' + str(temp_min) +'\n'+ 'Maximum Temperature(in Celsius) :'+str(temp_max)+'\n'+ "Humidity :" + humidity + "\nWind Speed :" + wind_speed
    return {
        'fulfillmentText': speech,
        'displaytext': speech
    }

if __name__=='__main__':
    app.run()
