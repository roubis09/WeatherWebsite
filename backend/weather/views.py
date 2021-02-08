from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import status
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *

# @api_view(http_method_names=["GET", "POST"])
def Forecast(location):
    forecast_url = "http://api.weatherapi.com/v1/forecast.json?key=cc1f71266946419a8ce52142201410&q={}&days=10"
    # location = 'kolkata'
    forecast_data = requests.get(forecast_url.format(location)).json()
    # print(len(forecast_data))
    if forecast_data:
        days = []
        for i in range(len(forecast_data)):
            day = {}
            day['date'] = forecast_data['forecast']['forecastday'][i]['date']
            day['avg_temp'] = forecast_data['forecast']['forecastday'][i]['day']['avgtemp_c']
            day['condition'] = forecast_data['forecast']['forecastday'][i]['day']['condition']['text']
            day['condition_icon'] = forecast_data['forecast']['forecastday'][i]['day']['condition']['icon']
            day['humidity'] = forecast_data['forecast']['forecastday'][i]['day']['avghumidity']
            day['chance_of_rain'] = forecast_data['forecast']['forecastday'][i]['day']['daily_chance_of_rain']
            day['sunrise'] = forecast_data['forecast']['forecastday'][i]['astro']['sunrise']
            day['sunset'] = forecast_data['forecast']['forecastday'][i]['astro']['sunset']
            # day.append(date)
            # day.append(avg_temp)
            days.append(day)
        # print(days)
        return days
            # data = {
            #     "day": forecast_data['forecast']['forecastday'][0]['date']       # 0 is for first day
            # }
        # print(days)
        # return Response(data={
        #     "data1": days
        # })


@api_view(http_method_names=["GET", "POST"])
def Home(request, location):
    # if request.method == "POST":
    if location:
        # forecast()
        # data = request.data
        # try:
        #     print(data['location'])
        # location = data['location']
        # print(location)
        # except:
        #     print("Error")
        #     return Response(data={
        #         "Status": "error",
        #     })

        # print(location)
        # print('**************')

        # location_url = 'http://dataservice.accuweather.com/locations/v1/cities/search?apikey=i8hpO8p3R5xuNyBtWHIAE5lSmJtobcxS&q={}'
        location_url = 'http://api.weatherapi.com/v1/current.json?key=cc1f71266946419a8ce52142201410&q={}'
        try:
            location_data = requests.get(location_url.format(location)).json()
            # print(location_data)


            if location_data:
                # city_data = {
                #     "message": "working",
                #     "location_name": str(location_data[0]["EnglishName"]),
                #     "Country": str(location_data[0]["Country"]["EnglishName"]),
                #     "state": str(location_data[0]["AdministrativeArea"]["EnglishName"]),
                #     "latitude": str(location_data[0]["GeoPosition"]["Latitude"]),
                #     "longitude": str(location_data[0]["GeoPosition"]["Longitude"]),
                #     "location_key": str(location_data[0]["Key"])
                # }

                city_data = {
                    "message": "working",
                    "location_name": str(location_data['location']['name']),
                    "Country": str(location_data['location']['country']),
                    "state": str(location_data['location']['region']),
                    "latitude": str(location_data['location']['lat']),
                    "longitude": str(location_data['location']['lon']),
                    "date": str(location_data['location']['localtime'].split(" ")[0]),
                    "time": str(location_data['location']['localtime'].split(" ")[1]),
                }

                # print(city_data)

                # weather_url = 'http://dataservice.accuweather.com/currentconditions/v1/' + city_data[
                #     "location_key"] + '?apikey=i8hpO8p3R5xuNyBtWHIAE5lSmJtobcxS&details=true'

                # weather_data = requests.get(weather_url).json()
                # print(weather_data)
                # weather_data = {
                #     "temp": str(weather_data[0]["Temperature"]["Metric"]["Value"]), # Imperial
                #     "real_temp": str(weather_data[0]["RealFeelTemperature"]["Metric"]["Value"]),
                #     "text": str(weather_data[0]["WeatherText"]),
                #     "WeatherIcon": int(weather_data[0]["WeatherIcon"]),
                #     "RelativeHumidity": int(weather_data[0]["RelativeHumidity"]),
                #     "Wind": int(weather_data[0]["Wind"]["Speed"]["Metric"]["Value"]),
                #     "Wind_Unit": str(weather_data[0]["Wind"]["Speed"]["Metric"]["Unit"]),
                #     "Pressure": int(weather_data[0]["Pressure"]["Metric"]["Value"]),
                #     "Pressure_Unit": str(weather_data[0]["Pressure"]["Metric"]["Unit"]),
                #     "UVIndex": int(weather_data[0]["UVIndex"]),
                #     "UVIndexText": str(weather_data[0]["UVIndexText"]),
                #     "CloudCover": int(weather_data[0]["CloudCover"]),
                # }
                weather_data = {
                    "temp": str(location_data['current']['feelslike_c'])+ ' °C',
                    "real_temp": str(location_data['current']['temp_c'])+ ' °C',
                    "condition": str(location_data['current']['condition']['text']),
                    "WeatherIcon": str(location_data['current']['condition']['icon']),
                    "RelativeHumidity": str(location_data['current']['humidity']),
                    "Wind": str(location_data['current']['wind_kph']),
                    "Pressure": str(location_data['current']['pressure_mb'])+ ' mb',
                    "CloudCover": str(location_data['current']['cloud']),


                }
                # print(weather_data)
                sun_url_api = "http://api.weatherapi.com/v1/forecast.json?key=cc1f71266946419a8ce52142201410&q={}"
                sun_url_data = requests.get(sun_url_api.format(location)).json()

                sun = {
                    "sunrise": str(sun_url_data['forecast']['forecastday'][0]['astro']['sunrise']),
                    "sunset": str(sun_url_data['forecast']['forecastday'][0]['astro']['sunset']),
                }
                # print(sun)
                forecast = Forecast(location)
                # print(forecast)
                return Response(data={
                    "Status": "working",
                    "Loc": location,
                    "location": city_data,
                    "weather": weather_data,
                    "sun": sun,
                    "forecast": forecast
                })

        # elif location_data['error']['code'] == 1006:
        except:
            # print(location_data)
            # print(location_data['error']['message'])
            msg = location_data['error']['message']
            # print(msg)
            return Response(data={
                "Error": msg,
            })




