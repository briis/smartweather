# List of Changes

### Version 0.1.9.1
* Change structure of repository to support [HACS](https://custom-components.github.io/hacs/)

### Version 0.1.9
* Removed Precipitation Last 24hr, as this data is no longer available in the REST API from WeatherFlow

### Version 0.1.8
* Optimized Custom Updater, so that there is only **one** entry, and that all files are updated at the same time.

### Version 0.1.7
* Added `manifest.json` to ensure compliance with Home Assistant >= 0.92.x. If Custom Updater is not the latest version, this file needs to be downloaded manually before upgrading

### Version 0.1.6
* Added configuration option for Wind Unit, when Home Assistant Unit System is metric. You can now specify if you want Wind Units in km/h. Default for metric is m/s and for Imperial it is mph. See README.md for information on how to set this up.

### Version 0.1.5
* Bumped pysmartweatherio to V0.1.8, where the component now handles when either AIR or SKY unit is not installed.

### Version 0.1.4
* Bumped pysmartweatherio to V0.1.5, which fixes a problem when a brand new station is used.

### Version 0.1.3
* Fixed Temperature error in the Weather Card, when using Imperial Units

### Version 0.1.2
* Updated the Icons for the Lightning Sensors
* Fixed Rain Rate too low
* Bumped *pysmartweatherio* to V0.1.3

### Version 0.1.0
* The smartweatherio part of this module has now converted to a PyPi module, so that it will be downloaded automatically during first run. That means that the subsirectory *smartweatherio* and all the files in there can be deleted.
* More code cleanup, to conform to the Style Guidelines in Home Assistant

### Version 0.0.5
* Added new Sensor *lightning_count*. Displaying how many lightning strikes have occurred within the last minute. This sensor has some extra Attributes describing when a lightning was last detected, the distance away from the Weather Station and how many lightning strikes were detected within the last 3 hours.<br>
**Please note**: Depending of the placement of the sensor, it might sometimes produce false positives.
* Added new Sensor *wind_lull*. This shows the lowest wind recorded within the last minute.
* Added new Binary Sensor *lightning*. True if a lightning strike has occurred within the last minute.
* Updated README.md with more descriptions and added the new Sensors
* More code clean-up

### Version 0.0.4
* Fixed Config Validation error
* Removed the DEVICE_CLASS for the Binary Sensors, as the value they gave was not really covering what this sensor was showing.
* Added 2 decimals to precipitation_rate, to get better accuracy
