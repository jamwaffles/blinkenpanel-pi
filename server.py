from neopixel import *

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 80

LED_COUNT = 60
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 5
LED_BRIGHTNESS = 32
LED_INVERT = False

class myHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/sns/basin":
            print "Got request to /sns/basin"

            self.send_response(200)
            self.end_headers()
            return

try:
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

    strip.begin()

    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 32, 0))

    strip.show()

    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER

    server.serve_forever()

except KeyboardInterrupt:
    print ' received, shutting down the web server'
    server.socket.close()
