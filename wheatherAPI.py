import requests

def current_weather_api():
    url = "https://api.open-meteo.com/v1/forecast?latitude=45.33&longitude=14.44&current_weather=true&timezone=auto"
    response = requests.get(url)
    data = response.json()

    return f"{data['current_weather']['temperature']}"