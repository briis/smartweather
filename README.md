# Smart Weather for Home Assistant
![WeatherFlow Logo](https://github.com/briis/hass-SmartWeather/blob/master/images/weatherflow.png)<br>
This a *custom component* for [Home Assistant](https://www.home-assistant.io/). It combines real-time weather readings from a Smart Weather weather station produced by *WeatherFlow* and Forecast data from *Dark Sky*.

It can create several `sensor` entities for each weather reading like Temperature, Precipitation, Rain etc. and it can create two `binary_sensor`, one indicating if it freezes outside and one indicating if it is raining. Finally it can also create a `weather` component, that then combines the real-time readings from the Weather Station and the Forecast data from Dark Sky, in to a standard `weather`component. 

The `smartweather` component uses the [WeatherFlow](https://weatherflow.github.io/SmartWeather/api/swagger/) REST API to retrieve current data for a local WeatherStation, and it uses [Dark Sky](https://darksky.net/dev) to retrieve Forecast data if the `weather` component is activated.

## Installation
1. If you don't already have a `custom_component` directory in your config directory, create it, and then create a directory called `smartweather`under that.
2. Copy all the files from this repository in to the *smartweather* folder. Remember to maintain the directory structure.

## Configuration
Start by configuring the base component. No matter which of the entities you activate, this has to be configured.

Edit your *configuration.yaml* file and add the *smartweather* component to the file:
```yaml
# Example configuration.yaml entry
smartweather:
  station_id: <your station id>
```
If you have your own Smart Weather Station, then you know your Station ID. If you don't have one, there are a lot of public stations available, and you can find one near you on [this link](https://smartweather.weatherflow.com/map). If you click on one of the stations on the map, you will see that the URL changes, locate the number right after */map/* - this is the Station ID

### Binary Sensor
In order to use the Binary Sensors, add the following to your *configuration.yaml* file:
```yaml
# Example configuration.yaml entry
binary_sensor:
  platform: smartweather
  monitored_conditions:
    - raining
    - freezing
```
#### Configuration Variables
   **name**<br>
   (string)(Optional)Additional name for the sensors.<br>
   Default value: SmartWeather
   
   **monitored_conditions**<br>
   (list)(optional)Sensors to display in the frontend.<br>
   Default: All Sensors are displayed
   * **raining** - A sensor indicating if it is currently raining
   * **freezing** - A sensor indicating if it is currently freezing outside.

### Sensor
In order to use the Sensors, add the following to your *configuration.yaml* file:
```yaml
# Example configuration.yaml entry
sensor:
  platform: smartweather
  monitored_conditions:
    - temperature
    - feels_like_temperature
    - heat_index
    - wind_chill
    - dewpoint
    - wind_speed
    - wind_gust
    - wind_bearing
    - wind_direction
    - precipitation
    - precipitation_rate
    - precipitation_last_1hr
    - precipitation_last_24hr
    - precipitation_yesterday
    - humidity
    - pressure
    - uv
    - solar_radiation
```
#### Configuration Variables
   **name**<br>
   (string)(Optional)Additional name for the sensors.<br>
   Default value: SmartWeather
   
   **monitored_conditions**<br>
   (list)(optional)Sensors to display in the frontend.<br>
   Default: All Sensors are displayed
   * **temperature** - Current temperature
   * **feels_like_temperature** - How the temperature Feels Like. A combination of Heat Index and Wind Chill
   * **heat_index** - A temperature measurement combining Humidity and temperature. How hot does it feel. Only used when temperature is above 26.67°C (80°F)
   * **wind_chill** - How cold does it feel. Only used if temperature is below 10°C (50°F)
   * **dewpoint** - Dewpoint. The atmospheric temperature (varying according to pressure and humidity) below which water droplets begin to condense and dew can form
   * **wind_speed** - Current Wind Speed
   * **wind_gust** - Current Wind Gust
   
