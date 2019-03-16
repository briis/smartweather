# List of Changes

### Version 0.0.5
* Added Lightning Sensors, displaying how many Lightnings have occurred and the approximate distance. This sensor has some extra Attributes describing when a lightning was last detected, the distance away from the Weather Station and how many lightnings were detected within the last 3 hours.
Under monitored conditions specify:
```yaml
sensor:
  - platform: smartweather
    monitored_conditions:
      - lightning
```
* Updated README.md with more descriptions

### Version 0.0.4
* Fixed Config Validation error
* Removed the DEVICE_CLASS for the Binary Sensors, as the value they gave was not really covering what this sensor was showing.
* Added 2 decimals to precipitation_rate, to get better accuracy
