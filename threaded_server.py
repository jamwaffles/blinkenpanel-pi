import math
from neopixel import *
import threading

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 80

LED_COUNT = 60
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 5
LED_BRIGHTNESS = 32
LED_INVERT = False

num_reqs = 0

framebuffer = [0 for x in range(LED_COUNT)]

def wheel(pos):
    return Color(
        int((1 + math.sin(pos * 0.1324)) * 127),
        int((1 + math.sin(pos * 0.1654)) * 127),
        int((1 + math.sin(pos * 0.1)) * 127)
    )

class myHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global num_reqs 

        if self.path == "/sns/basin":
            print "Got request to /sns/basin"

            num_reqs += 1

            for i in range(num_reqs):
		framebuffer[i] = wheel(i + num_reqs * 2)

            #strip.show()

            print "%s events received" % num_reqs

            self.send_response(200)
            self.end_headers()
            return

def runframe():
	threading.Timer(1.0 / 60, runframe).start()
	
	for i, val in enumerate(framebuffer):
		strip.setPixelColor(i, val)

	strip.show()

try:
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

    strip.begin()

    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 32, 0))

    strip.show()

    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER

    runframe()

    server.serve_forever()

except KeyboardInterrupt:
    print ' received, shutting down the web server'
    server.socket.close()
