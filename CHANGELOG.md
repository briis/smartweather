### V2.0.5

* Added two new Attributes to Weather Card `today_high_temp` and `today_low_temp` which gives the forecasted High and Low temperature for the current day.
* Based on latest information from WeatherFlow, the Condition Icons have now been finalized. That will fix Issue #44
* Forecasted precipitation is now reported as null, if there is now precipitation expected. This is the standard used throughout Home Assistant. Fixing Issue #45

### V2.0.4

* Fixed crash when returned sensor value was None - Issue #42
* Added Norwegian translation for Config Flow (Thanks to @hwikene)
* Added Danish translation for Config Flow
* Updated README, with a Section on what Sensors are being added to Home Assistant
