from flask import Flask, request, make_response
import pyowm
import json, os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
ownkey = '1b37dde14785c8d4061fef7f6c38f8c0'
own = pyowm.OWM(ownkey)


@app.route('/webhook', methods=['POST'])
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
    mgr = own.weather_manager()
    observation = mgr.weather_at_place(city)
    w = observation.weather
    temp_dict_kelvin = w.temperature()  # a dict in Kelvin units (default when no temperature units provided)
    temp_min = temp_dict_kelvin['temp_min']
    temp_max = temp_dict_kelvin['temp_max']
    speech = 'Today weather report :'+'\n'+'Temperature(Min---Max)' + str(temp_min) + " "+str(temp_max)
    return {
        'fulfillmentText': speech,
        'displaytext': speech
    }

if __name__=='__main__':
    app.run()