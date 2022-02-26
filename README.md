# Arduino Monitoring

<image src="./ArduinoMonitoring.jpg" width="400px">

I've created this project so I can collect and monitor real-time data from the drumming practice space I rent. This data is collected via an Arduino Pro Mini 3.3v equipped with sensors to measure PIR motion (to detect if anyone is using the space at any given time), humidity, temperature and light levels. Thanks to some of the techniques highlighted in <a href="https://diyi0t.com/arduino-reduce-power-consumption/#elementor-toc__heading-anchor-9" target="_blank">this article</a> I've managed to modify the Arduino to work for approximately 6 months off of 3 AA batteries.

The biggest obstacle to this project was the lack of WiFi within the practice space. To address this issue, the Arduino uses a radio breakout board to transmit data at regular intervals to a Raspberry Pi (approximately 2km away within an urban environment) which uploads the data to <a href="https://thingspeak.com/channels/1640336" target="_blank">this ThingSpeak channel</a>.
