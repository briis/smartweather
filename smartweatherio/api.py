import requests

from .models import WeatherData

def _url(stationid, apikey):
    return 'https://swd.weatherflow.com/swd/rest/observations/station/' + str(stationid) + '?api_key=' + str(apikey)

def load_weatherdata(stationid, apikey, units='metric', callback=None):
    """
    This Function builds the URL and returns the
    data from WeatherFlow. You will need to supply a Station Id and
    if you don't have your own station, you can find a list of public
    available stations here: https://smartweather.weatherflow.com/map
    """

    return get_weather(_url(stationid, apikey), units)

def get_weather(requestURL, units):
    data_reponse = requests.get(requestURL)
    data_reponse.raise_for_status()

    json = data_reponse.json()
    headers = data_reponse.headers

    return WeatherData(json, data_reponse, headers, units)
