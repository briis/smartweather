# List of Changes

### Version 0.0.5
* Added new Sensor *lightning_count*. Displaying how many Lightnings have occurred within the last minute and the approximate distance. This sensor has some extra Attributes describing when a lightning was last detected, the distance away from the Weather Station and how many lightnings were detected within the last 3 hours.
* Added new Sensor *wind_lull*. This shows the lowest wind recorded within the last minute.
* Added new Binary Sensor *lightning*. True if a lightning strike has occurred within the last minute.
* Updated README.md with more descriptions and added the new Sensors
* More code clean-up

### Version 0.0.4
* Fixed Config Validation error
* Removed the DEVICE_CLASS for the Binary Sensors, as the value they gave was not really covering what this sensor was showing.
* Added 2 decimals to precipitation_rate, to get better accuracy
