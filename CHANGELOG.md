### V2.2

*Released January 7th, 2021*

* `ADDED` New sensor called `sensor.smartweather_air_density` showing the recorded Air Density at the station.
* `ADDED` New sensor called `sensor.smartweather_sea_level_pressure` showing the Sea Level Pressure as opposed to the Station Pressure.

### V2.1

*Released December 19th, 2020*

* `FIXED` Pouring was shown as condition and icon, when WeatherFlow was reporting *rainy*. The *pouring* condition does not exist in the API, so this has been removed, and *rainy* will now be the default value.
* `ADDED`: There is now a new sensor being created for each battery powered HW device attached to the Hub. This sensor shows the current Volt for each of the devices. The sensor will update its state every hour. Closing Issue #46

### V2.0.5

* Added two new Attributes to Weather Card `today_high_temp` and `today_low_temp` which gives the forecasted High and Low temperature for the current day.
* Based on latest information from WeatherFlow, the Condition Icons have now been finalized. That will fix Issue #44
* Forecasted precipitation is now reported as null, if there is now precipitation expected. This is the standard used throughout Home Assistant. Fixing Issue #45

### V2.0.4

* Fixed crash when returned sensor value was None - Issue #42
* Added Norwegian translation for Config Flow (Thanks to @hwikene)
* Added Danish translation for Config Flow
* Updated README, with a Section on what Sensors are being added to Home Assistant
