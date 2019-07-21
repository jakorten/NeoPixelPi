#!/usr/bin/python3

"""
  Python 3 script to run a simple REST server for remotely controlling a LED (WS2812) strip.
  Johan Korten
  July 2019
"""
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import board
import neopixel

hostName = ""
hostPort = 80

pixel_pin = board.D18
num_pixels = 30 # 1 meter

# some globals for RGB
r = 255
g = 255
b = 255

state = 0

brightness = 1.0
last_color = (r, g, b)

ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=brightness, auto_write=False, pixel_order=ORDER)

"""
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
"""

class NeoPixelServer(BaseHTTPRequestHandler):

	# method for GET request
	def do_GET(self):
		content = '<p>You accessed path: {}</p>'.format(self.path)
		response = self.processServerRequest(self.path)
		self.response(response)

	# POST method for submitting data.
	def do_POST(self):

		print( "incoming http POST: ", self.path )

		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
		post_data = self.rfile.read(content_length) # <--- Gets the data itself
		self.send_response(200)
		client.close()

	def response(self, content):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(bytes(content, "utf-8"))

	def stringToRGB(self, hexString):
		""" a hex string with three components into an (r, g, b) tuple """
		global last_color
		_hexStringLower = hexString.lower()
		print(_hexStringLower)
		try:
		  r, g, b = int(_hexStringLower[:2],16), int(_hexStringLower[2:4],16), int(_hexStringLower[4:],16)
		except:
		  return last_color
		return (r, g, b)

	def getBrightness(self):
		global last_color
		return (max(last_color) / 2.5)

	def setHex(self, color, remember):
		# expects tuple of 4 bytes
		global last_color
		pixels.fill(color)
		if (remember == True):
		  last_color = color
		pixels.show()

	def processServerRequest(self, path):
		global last_color
		global state

		if ("/on" in path):
		  self.setHex(last_color, True)
		  state = 1
		  return "OK"
		if ("/off" in path):
		  state = 0
		  self.setHex((0,0,0), False)
		  return "OK"
		if ("/set/" in path):
		  _hexString = path[5:]
		  last_color = self.stringToRGB(_hexString)
		  self.setHex(last_color, True)
		  return "OK"
		if ("/status" in path):
		  return str(state)
		if ("/color" in path):
		  _result = "{:02x}{:02x}{:02x}".format(r,g,b)
		  print(_result)
		  return _result
		if ("/bright" in path):
		  _brightness = self.getBrightness()
		  return str(_brightness)

		return "Unknown"



neoPixelServer = HTTPServer((hostName, hostPort), NeoPixelServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
	neoPixelServer.serve_forever()
except KeyboardInterrupt:
	pass

neoPixelServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
