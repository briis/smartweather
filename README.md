# //Smart Weather
![WeatherFlow Logo](https://github.com/briis/hass-SmartWeather/blob/master/images/weatherflow.png)<br>
This is a *Custom Integration* for [Home Assistant](https://www.home-assistant.io/). It combines real-time weather readings from a Personal Weather station produced by *WeatherFlow* and Forecast data also from Weatherflow. It uses the public [REST API](https://weatherflow.github.io/SmartWeather/api/swagger/) to pull data from Weatherflow.

![GitHub release](https://img.shields.io/github/release/briis/smartweather.svg)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

There is currently support for the following device types within Home Assistant:

* Weather
* Sensor
* Binary Sensor

Forecast data can be delivered as *hourly* or *daily* data. The Forecast API uses the same AI driven model as you can see in there own APP. A BIG thank you to @max-rousseau for doing the initial implementation of this.

**Note**: If you are a version 1.x user, please read the Upgrade section below before you install this.

## Installation

### HACS installation
This Integration is part of the default HACS store, so go to the HACS page and search for *SmartWeather*.

### Manual Installation

To add SmartWeather to your installation, create this folder structure in your /config directory:

`custom_components/smartweather`.

Then drop the following files into that folder:

```yaml
__init__.py
binary_sensor.py
config_flow.py
const.py
entity.py
manifest.json
sensor.py
strings.json
weather.py
translation (Directory with all files)
```

### Upgrade from version 1.x
**Please be aware** that the old sensor names and the new sensor names might not match. So if you use this in any Automations, Value Templates, Scripts etc. you will have to change those after adding the new component.

The integration has been rewritten, to use *Config Flow* as configuration option, so if you have a previous version installed, you must first remove that.

To upgrade perform the below steps in that order:
1. Edit the *yaml* files that contain references to `smartweather` and remove them from the file. (configuration.yaml and were ever you store `sensor`, `binary_sensor` and `weather` configuration)
2. Remove the Integration from HACS
3. Restart Home Assistant
4. When HA is back online go to HACS and install the new Version of *SmartWeather*
5. Restart Home Assistant
6. When HA is back online, go to *Configuration* and then *Integrations*, click the + sign in the bottom right, and search for SmartWeather.
7. Fill out the Configuration Options, and click *Submit*. You should now have all the Devices and Entities configured.

## Configuration
To add SmartWeather to your installation, go to the Integration page inside the configuration panel and add a Personal Weather station by providing the API Key and Station ID of yours or a another Weatherflow Weather Station.

During installation you will have the option of selecting if you want to:
* have Daily or Hourly based Forecast data
* use mps or km/h as wind unit if you use the Metric unit system
* set the interval for updating current data and forecast data

These settings can also be changed after you add the Integration, by using the *Options* link on the Integration widget.

You can configure more than 1 instance of the Integration by either using a different Station ID, og by using the same Station ID, but then a different Forecast Type (Daily / Hourly). If you select the last option de-select the check-box `Install individual sensors` as this will only create the same sensors two times.

### Token for SmartWeather
The WeatherFlow REST API requires a Token. Please [login with your account](https://tempestwx.com/settings/tokens) and create the token. Go to Settings and choose Data Authorizations (almost at the bottom). Create a personal access token and use that as Token (API key).

**Please Note**: The Token you create here will ONLY work with Stations that are registered under the same Login.

### Station ID
Each WeatherFlow Station you setup, will get a unique Station ID, this id is needed during configuration. To get your Station ID, [login with your account](https://tempestwx.com/settings/stations/), select the station on the list, and then click *Status*. Here you will find your Station ID.

## Sensors
For each Station ID you add, the following sensors are being added to Home Assistant:

* *air_density* - Air Density.
* *air_temperature* - Outside Temperature.
* *brightness* - Brightness in Lux
* *dew_point* - Outside Dewpoint.
* *feels_like* - Outside Feels Like Temp.
* *heat_index* - Outside Heat Index.
* *lightning_strike_last_time* - the date and time of last strike.
* *lightning_strike_last_distance* - the distance away of last strike.
* *lightning_strike_count* - the daily strike count.
* *lightning_strike_count_last_1hr* - the strike count last 1 hour.
* *lightning_strike_count_last_3hr* - the strike count last 3 hours.
* *precip_accum_last_1hr* - Precipition for the Last Hour.
* *precip_accum_local_day* - Precipition for the Day.
* *precip_accum_local_yesterday* - Precipition for Yesterday.
* *precip_rate* - current precipitaion rate.
* *precip_minutes_local_day* - Precipition Minutes Today.
* *precip_minutes_local_yesterday* - Precipition Minutes Yesterday.
* *pressure_trend* - The pressure trend in text form. (Only english)
* *relative_humidity* - relative Humidity.
* *solar_radiation* - Solar Radiation.
* *station_pressure* - Station Pressure.
* *sea_level_pressure* - Sea Level Pressure.
* *uv* - UV Index.
* *wind_avg* - Wind Speed Average.
* *wind_bearing* - Wind Bearing as Degree.
* *wind_chill* - Wind Chill Temperature.
* *wind_gust* - Wind Gust Speed.
* *wind_direction* - Wind Direction Compass Symbol.
* *battery_DEVICE_NAME* - Reporting the current Voltage of each unit attached to the Hub. There will be one sensor per device.

Default they are named: `sensor.smartweather_SENSORNAME`. They all have a Unique ID, so you can rename them to whatever you like afterwards.
