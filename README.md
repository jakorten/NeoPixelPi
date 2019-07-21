# NeoPixelPi
Controlling a NeoPixel LED strip using Raspberry Pi / Homebridge

I wanted to control a WS2812 LED strip aka a NeoPixel LED strip (adafruit) to be controlled using homebridge and a Raspberry Pi Zero W.

See the Python source in <a href="https://github.com/jakorten/NeoPixelPi/blob/master/pixelServer.py">pixelServer.py</a>

I use the https://www.npmjs.com/package/homebridge-neopixel package for homebridge to control the LED strip directly from the Pi Zero.
Note: I connected the LED strip to the power adapter (3A, enough for 30 LEDs plus a Pi Zero W).

See https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring.

Others have used intermediate solutions including the ESP8266:
https://www.studiopieters.nl/homebridge-neopixel-light/ but a. I did not have a ESP8266 lying around and b. thought it was too much overhead for me (I have a secondary pi running homebridge so could have used that one and replaced this Pi Zero W with an ESP8266 or something but well this works and this is what I had 'lying around').

