# import required modules
import requests, json
 
# Enter your API key here
api_key = "9dc73970faafde4beb008b5e93ca7ab1"
 
# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"
 
# Give city name
from app import cn
 
# complete_url variable to store
# complete url address
complete_url = base_url + "q=" + city_name + "&appid=" + api_key
 
# get method of requests module
# return response object
response = requests.get(complete_url)
 
# json method of response object
# convert json format data into
# python format data
x = response.json()
 
# Now x contains list of nested dictionaries
# Check the value of "cod" key is equal to
# "404", means city is found otherwise,
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
 
else:
    print(" City Not Found ")