# //Smart Weather
![WeatherFlow Logo](https://github.com/briis/hass-SmartWeather/blob/master/images/weatherflow.png)<br>
This is a *Custom Integration* for [Home Assistant](https://www.home-assistant.io/). It combines real-time weather readings from a Personal Weather station produced by *WeatherFlow* and Forecast data also from Weatherflow. It uses the public [REST API](https://weatherflow.github.io/SmartWeather/api/swagger/) to pull data from Weatherflow.

![GitHub release](https://img.shields.io/github/release/briis/smartweather.svg)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

There is currently support for the following device types within Home Assistant:

* Weather
* Sensor
* Binary Sensor

Forecast data can be delivered as *hourly* or *daily* data.

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
