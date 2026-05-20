import geocoder
from geopy.geocoders import Nominatim
import requests
from requests.structures import CaseInsensitiveDict
import os                                                                                                                                                                                                          
from dotenv import load_dotenv
from pathlib import Path
import math

load_dotenv(Path(".env"))
api_key = os.getenv("API_KEY")

def convert(kelvin:int):
    result = (kelvin - 273.15) * 1.8 + 32
    return round(result)

def get_usr_location():
    loc = geocoder.ip('me')
    x = loc.lat
    y = loc.lng
    return [x, y]

def get_temp_emoji(temp):
    emoji = "😛"
    if temp > 80:
        emoji = "🥵"
    elif temp > 70:
        emoji = "😎"
    elif temp < 35:
        emoji = "🥶"
    return emoji

def get_weather_coords():
    lat = get_usr_location()[0]
    lon = get_usr_location()[1]
    url = "https://api.openweathermap.org/data/2.5/weather?lat="+str(lat)+"&lon="+str(lon)+"&appid="+ str(api_key)

    response = requests.get(url)
    x = response.json()
    y = x["main"]
    #get current temperature
    temperature = convert(y["temp"])
    a = x["sys"]
    city = f"{x["name"]}, {a["country"]}"
    #get current weather description
    z = x["weather"]
    weather_desc = z[0]["description"]


    output = f"It is {temperature}°F with {weather_desc} in {city}. {get_temp_emoji(temperature)}"
    return output

print(get_weather_coords())