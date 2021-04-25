### V2.2.4

Released: April 25th, 2021

* `FIXED`: When using daily forecast, todays forecast was never delivered, due to a bug in the IO module. Fixing issue #67.
* `CHANGE`: Code has been cleaned up. Removing obsolete definitions and variables.
* `CHANGE`: Ensuring the integration works with 2021.5.x - several files changed

### V2.2.3

*Released March 7th, 2021*

* `FIXED`: Added version number to `manifest.json` as required by Home Assistant V2021.3.x
* `FIXED`: Issue #60. Lightning Strike Time is now displayed as device class `timestamp` and will as such act differently in Lovelace Cards.

### V2.2.2

*Released February 1st, 2021*

* `FIXED`: Issue #52, where 0 values were reported if there was a glitch in the retrival of data from WeatherFlow. Certain sensors, like the Pressure Sensors, will not update, until a valid numbers is received.
* `ADDED`: Issue #51 and #53. There is now the possibility to add the same Station ID twice, with a different Forecast Type. So if you want to both have the Daily and Hourly Forecast data, then add the station again, but this time select the Forecast Type you did not have setup already. I recommend that on the second install, you de-select the check-box `Install individual sensors` so that you don't get the sensors double.

### V2.2.1

*Released January 9th, 2021*

* `FIXED`: WeatherFlow has released a new version of their Forecast API, which removed some fields, causing the Integration to fail. This is corrected with this Hotfix.

### V2.2

*Released January 7th, 2021*

* `ADDED` New sensor called `sensor.smartweather_air_density` showing the recorded Air Density at the station.
* `ADDED` New sensor called `sensor.smartweather_sea_level_pressure` showing the Sea Level Pressure as opposed to the Station Pressure.
* `ADDED` New sensor called `sensor.smartweather_pressure_trend` showing the Pressure trend in text.
* `ADDED` New sensor called `sensor.smartweather_lightning_last_1hrs` showing the number of Lightnings strikes for the last 1 hour

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
