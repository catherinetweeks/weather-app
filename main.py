from nicegui import ui
import geocoder
from geopy.geocoders import Nominatim
import requests
from requests.structures import CaseInsensitiveDict
import os                                                                                                                                                                                                          
from dotenv import load_dotenv
from pathlib import Path

#load in API key
load_dotenv(Path(".env"))
api_key = os.getenv("API_KEY")

#title the web page
ui.page_title('weather')

#function to get user's location at button press
def get_usr_location():
    loc = geocoder.ip('me')
    x = loc.lat
    y = loc.lng
    return [x, y]

# #function to allow user to input own location
# def get_input_location(input):
#     pass

#function that converts kelvin to fahrenheit
def convert(kelvin:int):
    result = (kelvin - 273.15) * 1.8 + 32
    return round(result)

#get appropriate emoji for temperature
def get_temp_emoji(temp):
    emoji = "😛"
    if temp > 80:
        emoji = "🥵"
    elif temp > 70:
        emoji = "😎"
    elif temp < 35:
        emoji = "🥶"
    return emoji

#function that calls the api to get the current weather
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

@ui.refreshable
def weather(input):
    ui.label(input).classes("text-lg")

#the card acts as a container for the title and buttons below it. I'm too used to divs I needed a faux-div.
with ui.card().classes('max-w-auto mx-auto mt-20 p-12 gap-12 no-shadow no-border items-center'):
    label = ui.label("what's the weather?").classes('text-h2 text-center')
    with ui.row():
        ui.button(icon="location_on", color="white", on_click=lambda: weather.refresh(get_weather_coords())).props("round unelevated").classes("p-5")
        enter_location = ui.input("city")
    #output the weather
    weather("") #initially empty


ui.run(favicon='🌁')