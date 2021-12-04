### V2.2.12

Released: 2021-12-04

**This Integration is now deprecated and will be replaced with a new Integration.**

This will be the last release of this integration. It was written a long time ago, and keeping it updated was more complicated than re-writing it from Scratch - which also gave me the possibility to add new stuff and ensure the code base adheres much better to Home Assistant coding practices.
Also the name *SmartWeather* was something used by WeatherFlow in the early days, today this name is gone more or less, so the new Integration is simply called [*WeatherFlow Weather*](https://github.com/briis/hass-weatherflow).
The new Integration is available now, but as I am waiting for my PR to merge in to the Default HACS store, you will right now have to add it as a *Custom Repository* to HACS.

**Changes**

* `FIX`: Issue #87, `device_state_attributes` are deprecated from V2021.12. This version migrates this to `extra_state_attributes`, and fixes this issue.
* `CHANGE`: To ensure this Integration follows the latest design principles, `state` has now been moved to `native_value`. This will have no direct effect for you as users.
* `NEW`: Added a Device Configuration Url, so that you can visit the Station Data directly from the Devices page. Requires Home Assistant 2021.11.

### V2.2.10

Released: October 17th, 2021

* `NEW`: Added `state_class` attributes to all sensors where applicable. A few more where added on top of what was in the last release.
* `FIX`: The *Rain Today* and *Rain minutes today* sensors have their state class changed, to reflect the correct sensor type. It should now work for showing the statistics.
* `FIX`: Issue #79 has been fixed. Rounding Fahrenheit units to 1 decimal.

Released: September 16th, 2021

* `NEW`: A new sensor called `sensor.smartweather_station_information` is now added. This sensor displays the Station Name in the state, but the Attributes contain more detailed information about the specific station, among these the Latitude and Longitude of the Station. Thank you to @jcgoette for implementing this.
* `NEW`: Added `state_class` attributes to selected sensors, so that they can be used with [Long Term Statistics](https://www.home-assistant.io/blog/2021/08/04/release-20218/#long-term-statistics).
* `CHANGE`: Other minor changes to support future HA versions.

### V2.2.8

Released: May 14th, 2021

* `FIXED`: High and Low temperature values were not converted to Fahrenheit when using Imperial Units. Fixing Issue #70
* `Fixed`: If using Imperial Units, the Pressure values are now more accurate, as the conversion formula has been updated and the number of decimals has been expanded to 3, when displaying the values. Fixing Issue #72

### V2.2.7

Released: May 12th, 2021

* `FIXED`: The Weather entity was using Station Pressure as the Pressure Value, but to align with the WeatherFlow App, this has now been changed to Sea Level Pressure. Fixing Issue #69


### V2.2.6

Released: May 4th, 2021

* `FIXED`: Added **iot_class** to `manifest.json` to comply with development requirements.


### V2.2.5

Released: April 26th, 2021

* `FIXED`: Datetime comparison error occurred when using Hourly Forecast method - issue #68. Fixed with this release.

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
