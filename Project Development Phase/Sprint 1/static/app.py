import flask
from flask import request, render_template 
from flask_cors import CORS 
import joblib
import requests, json
import math

# Enter your API key here
api_key = "9dc73970faafde4beb008b5e93ca7ab1"
 
# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"

app = flask. Flask(__name__, static_url_path='') 
CORS(app)

@app.route('/', methods=['GET']) 
def sendHomePage():
    return render_template("index.html")

 

@app.route('/predict', methods=['POST']) 
def predictSpecies():
    hwl = float(request.form['hwl']) 
    cn = input(request.form['cn']) 
    # complete_url variable to store complete url address
    complete_url = base_url + "q=" + cn + "&appid=" + api_key
    # get method of requests module 
    # return response object
    response = requests.get(complete_url)
 
    # json method of response object
    # convert json format data into python format data
    x = response.json()
 
    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to "404", means city is found otherwise,
    # city is not found
    if x["cod"] != "404":
 
        # store the value of "main"
        # key in variable y
        y = x["main"]
 
        # store the value corresponding
        # to the "temp" key of y
        current_temperature = y["temp"]
 
        # store the value corresponding
        # to the "pressure" key of y
        current_pressure = y["pressure"]
 
        # store the value corresponding
        # to the "humidity" key of y
        current_humidity = y["humidity"]

        #store the value of "wind"
        # key in variable a
        a = x["wind"]

        # store the value corresponding
        # to the "wind speed" key of a
        current_windspeed = a["speed"]
        current_winddeg = a["deg"]
 
        # store the value of "weather"
        # key in variable z
        z = x["weather"]
 
        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        weather_description = z[0]["description"]
 
        # print following values
        print(" Temperature (in kelvin unit) = " +
                    str(current_temperature) +
          "\n atmospheric pressure (in hPa unit) = " +
                    str(current_pressure) +
          "\n humidity (in percentage) = " +
                    str(current_humidity) +
          "\n description = " +
                    str(weather_description) +
          "\n wind speed (in meter per sec) = " + 
                    str(current_windspeed) +
          "\n wind direction (in degrees) = " + 
                    str(current_winddeg) )
        
        ws = ((current_windspeed * 1)/0.4) * math.log(10/0.5)
        wsten = ws/10
        ws = ((current_windspeed * 1)/0.4) * math.log(30/0.5)
        wsthirty = ws/30
        ws = ((current_windspeed * 1)/0.4) * math.log(50/0.5)
        wsfifty = ws/50
        wdten = float(current_winddeg)
        wdten+=wdten+ 1.0
        wdthirty = float(current_winddeg)
        wdfifty = float(current_winddeg )
        wdfifty+=wdfifty+4.0
        if(hwl<=10):
            wshwl = wsten
            wdhwl = wdten
        if(hwl>10 and hwl<=30):
            wshwl = wsthirty
            wdhwl = wdthirty
        elif(hwl>30 and hwl<=50):
            wshwl = wsfifty
            wdhwl = wdfifty
        else:
            wshwl = current_windspeed
            wdhwl = current_winddeg    
    else:
        print(" City Not Found ")

    x = [[wsten, wdten, wsthirty, wdthirty, wsfifty, wdfifty, wshwl, wdhwl, current_temperature, current_pressure, current_humidity]] 
    model = joblib.load('model.pkl')
    output = model.predict(x)[0]
    return render_template("predict.html", predict=output)

    if __name__ == '__main__':
        app.run()
