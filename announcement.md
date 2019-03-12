# Smart Weather for Home Assistant
![WeatherFlow Logo](https://github.com/briis/hass-SmartWeather/blob/master/images/weatherflow.png)<br>
This a *custom component* for [Home Assistant](https://www.home-assistant.io/). It combines real-time weather readings from a Smart Weather weather station produced by *WeatherFlow* and Forecast data from *Dark Sky*.

![GitHub release](https://img.shields.io/github/release-pre/briis/smartweather.svg)

It can create several `sensor` entities for each weather reading like Temperature, Precipitation, Rain etc. and it can create two `binary_sensor`, one indicating if it freezes outside and one indicating if it is raining. Finally it can also create a `weather` component, that then combines the real-time readings from the Weather Station and the Forecast data from Dark Sky, in to a standard `weather`component. 

The `smartweather` component uses the [WeatherFlow](https://weatherflow.github.io/SmartWeather/api/swagger/) REST API to retrieve current data for a local WeatherStation, and it uses [Dark Sky](https://darksky.net/dev) to retrieve Forecast data if the `weather` component is activated.

Please visit the Github Project for installation and Configuration options.

Only the `weather` entity will require a Dark Sky API Key, the SmartWeather component uses a public developer key, that you can get from WeatherFlow (See instructions on Github). You don't need to own your own Smart Weather weatherstation to use this component, as you can access many Public available stations around the world.

Personally I am totally new to `Python` programming, so I will welcome any constructive feedback on this component, and especially how, this could be done nicer than the code I have done - BUT it works, at least on my systems.
