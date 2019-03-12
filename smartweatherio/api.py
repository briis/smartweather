import requests
import threading

from .models import WeatherData

def _url(stationid, apikey):
    return 'https://swd.weatherflow.com/swd/rest/observations/station/' + str(stationid) + '?api_key=' + apikey

def load_weatherdata(stationid, apikey, units='metric', callback=None):
    """
    This Function builds the URL and returns the
    data from WeatherFlow. You will need to supply a Station Id and
    if you don't have your own station, you can find a list of public
    available stations here: https://smartweather.weatherflow.com/map
    """

    return manual(_url(stationid, apikey), units, callback=callback)

def manual(requestURL, units, callback=None):
    """
    This function is used by load_weatherdata OR by users to manually
    construct the URL for an API call.
    """

    if callback is None:
        return get_weather(requestURL, units)
    else:
        thread = threading.Thread(target=load_async,
                                  args=(requestURL, callback))
        thread.start()

def get_weather(requestURL, units):
    data_reponse = requests.get(requestURL)
    data_reponse.raise_for_status()

    json = data_reponse.json()
    headers = data_reponse.headers

    return WeatherData(json, data_reponse, headers, units)


def load_async(url, callback):
    callback(get_forecast(url))
