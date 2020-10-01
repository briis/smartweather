# //Smart Weather
![WeatherFlow Logo](https://github.com/briis/hass-SmartWeather/blob/master/images/weatherflow.png)<br>
This is a *Custom Integration* for [Home Assistant](https://www.home-assistant.io/). It combines real-time weather readings from a Personal Weather station produced by *WeatherFlow* and Forecast data also from Weatherflow. It uses the public [REST API](https://weatherflow.github.io/SmartWeather/api/swagger/) to pull data from Weatherflow.

![GitHub release](https://img.shields.io/github/release/briis/smartweather.svg)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

There is currently support for the following device types within Home Assistant:

* Weather
* Sensor
* Binary Sensor

Forecast data can be delivered as *hourly* or *daily* data. The Forecast API is still under development from WeatherFlow, so it might change over time. As it is right now, it is very stable and uses the same AI driven model as you can see in there own APP. A BIG thank you to @max-rousseau for doing the initial implementation of this.

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

#### API Key for SmartWeather
The WeatherFlow REST API requires a API Key, but for personal use, you can use a development key, which you can [find here](https://weatherflow.github.io/SmartWeather/api/#getting-started). Please note the restrictions applied. WeatherFlow is silently releasing a new Authorization flow, so in the future there will be an option to obtain your own personal key.

#### Station ID
If you have your own Smart Weather Station, then you know your Station ID. If you don't have one, there are a lot of public stations available, and you can find one near you on [this link](https://smartweather.weatherflow.com/map). If you click on one of the stations on the map, you will see that the URL changes, locate the number right after */map/* - this is the Station ID

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
* *lightning_strike_count_last_3hr* - the strike count last 3hr.
* *precip_accum_last_1hr* - Precipition for the Last Hour.
* *precip_accum_local_day* - Precipition for the Day.
* *precip_accum_local_yesterday* - Precipition for Yesterday.
* *precip_rate* - current precipitaion rate.
* *precip_minutes_local_day* - Precipition Minutes Today.
* *precip_minutes_local_yesterday* - Precipition Minutes Yesterday.
* *relative_humidity* - relative Humidity.
* *solar_radiation* - Solar Radiation.
* *station_pressure* - Station Pressure.
* *timestamp*  - Data Timestamp.
* *station_name* - Station Name.
* *uv* - UV Index.
* *wind_avg* - Wind Speed Average.
* *wind_bearing* - Wind Bearing as Degree.
* *wind_chill* - Wind Chill Temperature.
* *wind_gust* - Wind Gust Speed.
* *wind_direction* - Wind Direction Compass Symbol.
