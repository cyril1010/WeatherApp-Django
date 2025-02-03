import requests
from django.shortcuts import render
from datetime import datetime
from pytz import timezone

API_KEY = 'Use_your_key_here'

def home(request):
    return render(request, "home.html")

def get_weather(request):
    weather_data = None
    error_message = None
    time_data = None

    if request.method == "POST":
        city = request.POST.get("city")

        if city:
            try:
                # Fetch weather data from OpenWeatherMap
                url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
                response = requests.get(url)
                data = response.json()

                if data.get('cod') == 200:
                    weather_data = {
                        'city': data['name'],
                        'temperature': data['main']['temp'],
                        'description': data['weather'][0]['description'],
                        'icon': data['weather'][0]['icon'],
                        'latitude': data['coord']['lat'],
                        'longitude': data['coord']['lon'],
                        'timezone_offset': data['timezone'],  # timezone offset in seconds
                    }

                    # Calculate the local time using the timezone offset
                    utc_time = datetime.utcfromtimestamp(data['dt'])
                    local_time = utc_time.timestamp() + weather_data['timezone_offset']  # adjust to local time
                    local_time = datetime.fromtimestamp(local_time)  # convert to datetime object
                    weather_data['current_time'] = local_time.strftime('%Y-%m-%d %H:%M:%S')

                else:
                    error_message = "City not found or error fetching data."

            except requests.exceptions.RequestException as e:
                error_message = f"Error fetching data: {e}"

    context = {
        'weather_data': weather_data,
        'error_message': error_message
    }
    return render(request, 'home.html', context)
