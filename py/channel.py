import time
import logging


import twilio_api
import codec


class CodecChannel:
    def __init__(self, codec, cfg):
        self.codec = codec
        self.name = cfg['name']
        self.channel = cfg['channel']
        self.uri = cfg['uri']
        self.hook_tstamp = time.time() - 60
        self.slot = cfg['slot']
        self.hook_status = 'UNKNOWN'
        self.call_start = time.time() - 60
        self.vu = 0
        self.studio_light = 'DISABLED'


    def set_studio_light(self, mode):
        if mode in ['DISABLED', 'OFF-AIR', 'ON-AIR']:
            self.studio_light = mode


    def set_hook_status(self, status):
        if self.hook_status == 'CONNECTED' and status == 'DISCONNECTED':
            delta = time.strftime('%H:%M:%S', time.gmtime(time.time() - self.call_start))
            logging.info('{} is disconnected after {}'.format(self.name, delta))

        if self.hook_status != 'CONNECTED' and status == 'CONNECTED':
            self.call_start = time.time()

        if status in ['DISCONNECTED', 'DIALING', 'CONNECTED']:
            self.hook_status = status

        logging.info('{} is {}'.format(self.name, self.hook_status))

    def get_hook_status_from_codec(self):
        path = '/ve/channel/ahStatus?ch=' + self.channel
        out = self.codec.load_json(path)
        if out:
            if out['oh'] == 1:
                self.set_hook_status('CONNECTED')
            elif out['oh'] == 4:
                self.set_hook_status('DIALING')
            else:
                self.set_hook_status('DISCONNECTED')

            self.hook_tstamp = time.time()

    def channel_status(self):
        if (time.time() - self.hook_tstamp) < 4:
            return self.hook_status
        return 'UNKNOWN'

    def call(self):
        path = '/ve/channel/call?ch={}&uri={}'.format(self.channel, self.uri)
        out = self.codec.load_json(path)

    def drop(self):
        path = '/ve/channel/line?ch={}&oh=false'.format(self.channel)
        out = self.codec.load_json(path)

    def call_time(self):
        if self.hook_status == 'CONNECTED':
            delta = time.time() - self.call_start
            return time.strftime('%H:%M:%S', time.gmtime(delta))

        return '--:--:--'

    def twilio_conference(self):
        print("LOOKING FOR: {}".format(self.name))
        conf = twilio_api.get_conference_by_name(self.name)
        if conf:
            return conf.conference_json()
        return {}

    def combined_status(self):
        conf = twilio_api.get_conference_by_name(self.name)
        if conf:
            if self.channel_status() == 'CONNECTED' and conf.status() == 'CONNECTED':
                return 'CONNECTED'
        return 'DISCONNECTED'

    def ch_json(self):
        json_out = {
            'name': self.name, 'status': self.channel_status(),
            'slot': self.slot, 'vu': self.vu, 'call_time': self.call_time(),
            'studio_light': self.studio_light,
            'combined_status': self.combined_status()
        }
        conf = twilio_api.get_conference_by_name(self.name)
        if conf:
            conf_out = {
                'conf_status': conf.status(), 'conf_time': conf.call_time(),
                'conf_name': conf.name, 'conf_count': conf.call_count
            }
        else:
            conf_out = {
                'conf_status': 'NA', 'conf_time': '--:--:--',
                'conf_name': '', 'conf_count': 0
            }
        json_out.update(conf_out)
        return json_out
