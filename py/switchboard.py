import json
import asyncio
import logging

from tornado import websocket, web, ioloop, escape

import config
import callControl
from status import conferenceStatus


class IndexHandler(web.RequestHandler):
    def get(self):
        self.write("hi")

class JoinHandler(web.RequestHandler):
    def get(self):
        To = self.get_argument("To", default=None, strip=False)
        webrtc_language = self.get_argument("language", default=None, strip=False)
        self.set_header('Content-Type', 'text/xml')
        self.write(callControl.initialCall(To, webrtc_language))

class GatherHandler(web.RequestHandler):
    def get(self):
        To = self.get_argument("To", default=None, strip=False)
        Digits = int(self.get_argument("Digits", default=None, strip=False))
        self.set_header('Content-Type', 'text/xml')
        self.write(callControl.gatherDigits(To, Digits))

class HoldHandler(web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/xml')
        self.write(callControl.conferenceOnHold())

class CodecHandler(web.RequestHandler):
    def get(self):
        From = self.get_argument("From", default=None, strip=False)
        self.set_header('Content-Type', 'text/xml')
        self.write(callControl.codecConference(From))

class ControlHandler(web.RequestHandler):
    def get(self):
        global conferenceStatus
        self.set_header('Content-Type', 'text/json')
        self.write(json.dumps(conferenceStatus))

    def post(self):
        live = self.get_argument('live', default=None, strip=False)
        delay = self.get_argument('delay', default=None, strip=False)
        callControl.changeConferenceStatus(live, delay)
        self.write(json.dumps(conferenceStatus))

def twisted():
    app = web.Application([
        (r'/', IndexHandler),
        (r'/conference/join', JoinHandler),
        (r'/conference/gatherDigit', GatherHandler),
        (r'/conference/onHold', HoldHandler),
        (r'/conference/codecs', CodecHandler),
        (r'/conference/control', ControlHandler)
    ])
    # https://github.com/tornadoweb/tornado/issues/2308
    asyncio.set_event_loop(asyncio.new_event_loop())
    app.listen(config.config_tree['switchboard_port'])
    ioloop.IOLoop.instance().start()



def main():
    config.read_json_config(config.config_file())
    twisted()

if __name__ == '__main__':
    main()
