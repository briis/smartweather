from .utils import UnicodeMixin, PropertyUnavailable, Conversion
import datetime
import requests

class WeatherData(UnicodeMixin):
    def __init__(self, data, response, headers, units):
        self.response = response
        self.http_headers = headers
        self.json = data
        self.units = units.lower()

        self._alerts = []
        for alertJSON in self.json.get('alerts', []):
            self._alerts.append(Alert(alertJSON))

    def update(self):
        r = requests.get(self.response.url)
        self.json = r.json()
        self.response = r

    def currentdata(self):
        dtformat = datetime.datetime.fromtimestamp(self.json['obs'][0]['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        return CurrentData(
            self.json['station_name'],
            dtformat,
            self.json['obs'][0]['air_temperature'],
            self.json['obs'][0]['feels_like'],
            Conversion.speed(float(self.json['obs'][0]['wind_avg']), self.units),
            int(self.json['obs'][0]['wind_direction']),
            Conversion.wind_direction(self.json['obs'][0]['wind_direction']),
            Conversion.speed(float(self.json['obs'][0]['wind_gust']), self.units),
            float(self.json['obs'][0]['uv']),
            Conversion.volume(float(self.json['obs'][0]['precip_accum_local_day']), self.units),
            int(self.json['obs'][0]['relative_humidity']),
            Conversion.volume(float(self.json['obs'][0]['precip']), self.units),
            float(self.json['obs'][0]['precip']),
            Conversion.pressure(float(self.json['obs'][0]['barometric_pressure']), self.units),
            float(self.json['latitude']),
            float(self.json['longitude']),
            self.json['obs'][0]['heat_index'],
            self.json['obs'][0]['wind_chill'],
            self.json['obs'][0]['dew_point'],
            Conversion.volume(float(self.json['obs'][0]['precip_accum_last_1hr']), self.units),
            Conversion.volume(float(self.json['obs'][0]['precip_accum_last_24hr']), self.units),
            Conversion.volume(float(self.json['obs'][0]['precip_accum_local_yesterday']), self.units),
            int(self.json['obs'][0]['solar_radiation']),
            int(self.json['obs'][0]['brightness'])
            )

class Alert(UnicodeMixin):
    def __init__(self, json):
        self.json = json

    def __getattr__(self, name):
        try:
            return self.json[name]
        except KeyError:
            raise PropertyUnavailable(
                "Property '{}' is not valid"
                " or is not available for this forecast".format(name)
            )

    def __unicode__(self):
        return '<Alert instance: {0} at {1}>'.format(self.title, self.time)

class CurrentData:
    def __init__(self, station_location, timestamp, temperature, feels_like, wind_speed, wind_bearing, wind_direction, wind_gust,
                 uv, precipitation,humidity, precipitation_rate, rain_rate_raw, pressure, latitude, longitude, heat_index, wind_chill, dewpoint,
                 precipitation_last_1hr, precipitation_last_24hr, precipitation_yesterday, solar_radiation, brightness
                 ):
        self.station_location = station_location
        self.timestamp = timestamp
        self.temperature = temperature
        self.feels_like_temperature = feels_like
        self.wind_speed = wind_speed
        self.wind_bearing = wind_bearing
        self.wind_direction = wind_direction
        self.wind_gust = wind_gust
        self.uv = uv
        self.precipitation = precipitation
        self.humidity = humidity
        self.precipitation_rate = precipitation_rate
        self.pressure = pressure
        self.latitude = latitude
        self.longitude = longitude
        self.heat_index = heat_index
        self.wind_chill = wind_chill
        self.dewpoint = dewpoint
        self.precipitation_last_1hr = precipitation_last_1hr
        self.precipitation_last_24hr = precipitation_last_24hr
        self.precipitation_yesterday = precipitation_yesterday
        self.solar_radiation = solar_radiation
        self.illuminance = brightness

        if rain_rate_raw > 0:
            self.raining = True
        else:
            self.raining = False

        if temperature < 0:
            self.freezing = True
        else:
            self.freezing = False
