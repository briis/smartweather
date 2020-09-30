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
* set the interval for updating current data anf forecast data

These settings can also be changed after you add the Integration, by using the *Options* link on the Integration widget.