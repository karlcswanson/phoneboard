import json
import os
import asyncio
import socket
import logging


from tornado import websocket, web, ioloop, escape

import config
import jk_audio
import groups
import twilio_api

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render(config.app_dir("index.html"))

class JsonHandler(web.RequestHandler):
    def get(self):
        codecs = []
        for codec in jk_audio.audio_codecs:
            codecs.append(codec.codec_json())

        json_out = json.dumps({
            'config': config.config_tree, 'codecs': codecs
        }, sort_keys=True, indent=4)


        self.set_header('Content-Type', 'application/json')
        self.write(json_out)

class SocketHandler(websocket.WebSocketHandler):
    clients = set()

    def check_origin(self, origin):
        return True

    def open(self):
        self.clients.add(self)

    def on_close(self):
        self.clients.remove(self)

    @classmethod
    def broadcast(cls, data):
        for c in cls.clients:
            try:
                c.write_message(data)
            except:
                logging.warning("WS Error")

    @classmethod
    def ws_dump(cls):
        out = {}

        if jk_audio.data_update_list:
            out['data-update'] = []
            for ch in jk_audio.data_update_list:
                out['data-update'].append(ch.ch_json())

        if out:
            data = json.dumps(out)
            cls.broadcast(data)

        del jk_audio.data_update_list[:]


class ChannelAPIHandler(web.RequestHandler):
    def get(self, slot):
        json_out = {}
        ch = jk_audio.get_channel_by_slot(int(slot))
        if ch:
            json_out = ch.ch_json()
        self.set_header('Content-Type', 'application/json')
        self.write(json_out)

    def post(self, slot):
        json_out = {}
        ch = jk_audio.get_channel_by_slot(int(slot))
        cmd = self.get_argument("cmd", default=None, strip=False)
        if ch:
            if cmd == 'call':
                ch.call()
            if cmd == 'drop':
                ch.drop()

            if cmd == 'close_room':
                conf = ch.conf()
                if conf:
                    conf.close_room()

            if cmd == 'studio-light-disable':
                ch.set_studio_light('DISABLED')
            if cmd == 'studiolight-off-air':
                ch.set_studio_light('OFF-AIR')
            if cmd == 'studiolight-on-air':
                ch.set_studio_light('ON-AIR')

        self.set_header('Content-Type', 'application/json')
        self.write(json_out)

class ConferenceAPIHandler(web.RequestHandler):
    def get(self):
        active_conferences = []
        for conference in twilio_api.conference_list:
            active_conferences.append(conference.conference_json())

        json_out = json.dumps({
            'conferences': active_conferences
        }, sort_keys=True, indent=4)

        self.set_header('Content-Type', 'application/json')
        self.write(json_out)



class GroupAPIHandler(web.RequestHandler):
    def get(self, group_number):
        json_out = {}
        group = groups.get_group(int(group_number))
        if group:
            json_out = group.group_json()
        self.set_header('Content-Type', 'application/json')
        self.write(json_out)

    def post(self, group_number):
        json_out = {}
        group = groups.get_group(int(group_number))
        cmd = self.get_argument("cmd", default=None, strip=False)
        studio_light = self.get_argument("studio_light", default=None, strip=False)
        if group:
            if cmd == 'call':
                group.call()
            if cmd == 'drop':
                group.drop()

            if cmd == 'studiolight-disable':
                group.set_studio_light('DISABLED')
            if cmd == 'studiolight-off-air':
                group.set_studio_light('OFF-AIR')
            if cmd == 'studiolight-on-air':
                group.set_studio_light('ON-AIR')

        self.set_header('Content-Type', 'application/json')
        self.write(json_out)

class webRTCTokenHandler(web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/jwt')
        self.write(twilio_api.get_capability_token())

def twisted():
    app = web.Application([
        (r'/', IndexHandler),
        (r'/ws', SocketHandler),
        (r'/data', JsonHandler),
        (r'/api/channel/([0-9]+)', ChannelAPIHandler),
        (r'/api/group/([0-9]+)', GroupAPIHandler),
        (r'/api/conference/', ConferenceAPIHandler),
        (r'/api/auth_token', webRTCTokenHandler),
        (r'/static/(.*)', web.StaticFileHandler, {'path': config.app_dir('static')})
    ])
    # https://github.com/tornadoweb/tornado/issues/2308
    asyncio.set_event_loop(asyncio.new_event_loop())
    app.listen(config.web_port())
    ioloop.PeriodicCallback(SocketHandler.ws_dump, 50).start()
    ioloop.IOLoop.instance().start()
